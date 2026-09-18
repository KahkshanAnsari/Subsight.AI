"""
Supabase Service — Authentication and Persistent Storage for SubSight AI.

All Supabase interactions are isolated here:
  - Client initialization (lazy, robust loading from st.secrets / env)
  - User authentication (sign up / sign in / sign out)
  - Subscription CRUD (insert / update / delete / fetch)
  - Bulk operations (demo data load, clear all)

Design principles:
  - No st.* calls — this module is pure Python and fully testable.
  - Every public function returns (success: bool, data_or_error: Any).
  - Uses Supabase anon/public key + Row Level Security to enforce data isolation.
  - Uses the authenticated user's JWT (access_token) for all data operations,
    ensuring RLS policies bind correctly to auth.uid().
"""

from __future__ import annotations

import os
import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Client initialization & Credentials Handling
# ---------------------------------------------------------------------------

_PLACEHOLDER_PATTERNS = (
    "your-project",
    "your_project",
    "placeholder",
    "example",
    "<project-ref>",
    "<your-project-ref>",
    "<anon-public-key>",
    "<your-anon-key>",
)


def _load_credentials() -> Tuple[str, str, str]:
    """
    Load and validate SUPABASE_URL and SUPABASE_KEY from Streamlit secrets or environment.
    Supports root-level keys, lowercase aliases, and nested [supabase] TOML sections.

    Returns:
        (url, key, error_message)
        error_message is empty string ("") when credentials are valid.
    """
    url: str = ""
    key: str = ""

    # 1. Attempt loading from Streamlit secrets
    try:
        import streamlit as st
        # Check top-level keys with aliases
        url = (
            st.secrets.get("SUPABASE_URL")
            or st.secrets.get("supabase_url")
            or st.secrets.get("SUPABASE_PROJECT_URL")
            or ""
        )
        key = (
            st.secrets.get("SUPABASE_KEY")
            or st.secrets.get("supabase_key")
            or st.secrets.get("SUPABASE_ANON_KEY")
            or st.secrets.get("supabase_anon_key")
            or ""
        )

        # Check nested [supabase] section if present in secrets.toml
        if not url or not key:
            supabase_section = st.secrets.get("supabase") or st.secrets.get("SUPABASE") or {}
            if isinstance(supabase_section, dict):
                if not url:
                    url = (
                        supabase_section.get("SUPABASE_URL")
                        or supabase_section.get("url")
                        or supabase_section.get("URL")
                        or ""
                    )
                if not key:
                    key = (
                        supabase_section.get("SUPABASE_KEY")
                        or supabase_section.get("key")
                        or supabase_section.get("KEY")
                        or supabase_section.get("anon_key")
                        or supabase_section.get("SUPABASE_ANON_KEY")
                        or ""
                    )
    except Exception:
        pass

    # 2. Fall back to environment variables
    if not url:
        url = (
            os.environ.get("SUPABASE_URL")
            or os.environ.get("supabase_url")
            or os.environ.get("SUPABASE_PROJECT_URL")
            or ""
        )
    if not key:
        key = (
            os.environ.get("SUPABASE_KEY")
            or os.environ.get("supabase_key")
            or os.environ.get("SUPABASE_ANON_KEY")
            or os.environ.get("supabase_anon_key")
            or ""
        )

    # 3. Sanitize inputs (strip whitespace, surrounding quotes, and trailing slashes)
    url = str(url).strip().strip("'\"").rstrip("/")
    key = str(key).strip().strip("'\"")

    # 4. Strict Validation
    if not url:
        return "", "", (
            "SUPABASE_URL is missing. Please configure SUPABASE_URL in your Streamlit Cloud Secrets "
            "(or in .streamlit/secrets.toml for local development). "
            "Example: SUPABASE_URL = \"https://xxxxxxxxxxxxxxxxxxxx.supabase.co\""
        )

    # Check for placeholder indicators or angle brackets
    if "<" in url or ">" in url or any(p in url.lower() for p in _PLACEHOLDER_PATTERNS):
        return "", "", (
            f"SUPABASE_URL contains placeholder values ('{url}'). "
            "Please replace it with your real Supabase Project URL from: "
            "Supabase Dashboard → Project Settings → API → Project URL."
        )

    if not url.startswith("https://"):
        return "", "", (
            f"SUPABASE_URL must start with 'https://' (got: '{url}'). "
            "Example: https://xxxxxxxxxxxxxxxxxxxx.supabase.co"
        )

    if not key:
        return "", "", (
            "SUPABASE_KEY is missing. Please configure SUPABASE_KEY in your Streamlit Cloud Secrets "
            "(or in .streamlit/secrets.toml for local development). "
            "Find it in Supabase Dashboard → Project Settings → API → Project API Keys (anon/public)."
        )

    if "<" in key or ">" in key or any(key.lower().startswith(p) for p in ("your-anon", "your-service", "placeholder")):
        return "", "", (
            "SUPABASE_KEY contains a placeholder value. "
            "Please copy your actual Supabase 'anon' public key from Project Settings → API."
        )

    return url, key, ""


def get_supabase_client():
    """
    Lazy-initialize and return a Supabase client.
    Returns None if credentials are missing or invalid.
    """
    url, key, err = _load_credentials()
    if err or not url or not key:
        return None

    try:
        from supabase import create_client, Client
        client: Client = create_client(url, key)
        return client
    except Exception:
        return None


def is_supabase_configured() -> bool:
    """Return True if real (non-placeholder) Supabase credentials are available."""
    _, _, err = _load_credentials()
    return err == ""


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def sign_up(email: str, password: str, display_name: str = "") -> Tuple[bool, Optional[Dict], str]:
    """
    Register a new user with Supabase Auth.

    Returns:
        (True, user_dict, "") on success
        (False, None, error_message) on failure
    """
    url, key, cred_err = _load_credentials()
    if cred_err:
        return False, None, cred_err

    client = get_supabase_client()
    if client is None:
        return False, None, "Could not initialize Supabase client. Please check SUPABASE_URL and SUPABASE_KEY."

    try:
        metadata: Dict[str, Any] = {}
        if display_name.strip():
            metadata["display_name"] = display_name.strip()
            metadata["full_name"] = display_name.strip()

        credentials: Dict[str, Any] = {
            "email": email.strip().lower(),
            "password": password,
        }
        if metadata:
            credentials["options"] = {"data": metadata}

        response = client.auth.sign_up(credentials)

        if response.user is None:
            return False, None, "Sign-up did not return a user. Please try again."

        user_dict = _extract_user_dict(response.user, response.session)
        return True, user_dict, ""

    except Exception as exc:
        raw = str(exc)
        return False, None, _friendly_auth_error(raw, include_raw=True)


def sign_in(email: str, password: str) -> Tuple[bool, Optional[Dict], str]:
    """
    Authenticate an existing user with email/password.

    Returns:
        (True, user_dict, "") on success
        (False, None, error_message) on failure
    """
    url, key, cred_err = _load_credentials()
    if cred_err:
        return False, None, cred_err

    client = get_supabase_client()
    if client is None:
        return False, None, "Could not initialize Supabase client. Please check SUPABASE_URL and SUPABASE_KEY."

    try:
        response = client.auth.sign_in_with_password({
            "email": email.strip().lower(),
            "password": password,
        })

        if response.user is None:
            return False, None, "Invalid email or password. Please try again."

        user_dict = _extract_user_dict(response.user, response.session)
        return True, user_dict, ""

    except Exception as exc:
        raw = str(exc)
        return False, None, _friendly_auth_error(raw, include_raw=True)


def sign_out(access_token: str = "") -> Tuple[bool, str]:
    """
    Sign out the current user and invalidate their session.

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    client = get_supabase_client()
    if client is None:
        return True, ""  # No client — treat as already signed out

    try:
        client.auth.sign_out()
        return True, ""
    except Exception:
        # Even if sign-out fails on server, clear local state
        return True, ""


# ---------------------------------------------------------------------------
# Subscription CRUD
# ---------------------------------------------------------------------------

def get_user_subscriptions(user_id: str, access_token: str) -> Tuple[bool, List[Dict], str]:
    """
    Fetch all subscriptions for the authenticated user.

    Returns:
        (True, list_of_sub_dicts, "") on success
        (False, [], error_message) on failure
    """
    client = _get_authed_client(access_token)
    if client is None:
        return False, [], "Database connection unavailable."

    try:
        response = (
            client.table("subscriptions")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=False)
            .execute()
        )
        rows = response.data or []
        subs = [_map_db_row_to_sub_dict(row) for row in rows]
        return True, subs, ""
    except Exception as exc:
        return False, [], _friendly_db_error(str(exc))


def insert_subscription(user_id: str, sub_dict: Dict, access_token: str) -> Tuple[bool, str]:
    """
    Insert a single new subscription for the authenticated user.

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    client = _get_authed_client(access_token)
    if client is None:
        return False, "Database connection unavailable."

    try:
        row = _map_sub_dict_to_db_row(user_id, sub_dict)
        client.table("subscriptions").insert(row).execute()
        return True, ""
    except Exception as exc:
        return False, _friendly_db_error(str(exc))


def upsert_subscription(user_id: str, sub_dict: Dict, access_token: str) -> Tuple[bool, str]:
    """
    Insert or update a single subscription (upsert on primary key `id`).

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    client = _get_authed_client(access_token)
    if client is None:
        return False, "Database connection unavailable."

    try:
        row = _map_sub_dict_to_db_row(user_id, sub_dict)
        client.table("subscriptions").upsert(row, on_conflict="id").execute()
        return True, ""
    except Exception as exc:
        return False, _friendly_db_error(str(exc))


def delete_subscription(user_id: str, sub_id: str, access_token: str) -> Tuple[bool, str]:
    """
    Delete a single subscription by ID, scoped to the authenticated user.

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    client = _get_authed_client(access_token)
    if client is None:
        return False, "Database connection unavailable."

    try:
        (
            client.table("subscriptions")
            .delete()
            .eq("id", sub_id)
            .eq("user_id", user_id)
            .execute()
        )
        return True, ""
    except Exception as exc:
        return False, _friendly_db_error(str(exc))


def delete_all_user_subscriptions(user_id: str, access_token: str) -> Tuple[bool, str]:
    """
    Delete ALL subscriptions belonging to the authenticated user.
    Used by "Clear Data" and "Clear Demo Data" actions.

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    client = _get_authed_client(access_token)
    if client is None:
        return False, "Database connection unavailable."

    try:
        (
            client.table("subscriptions")
            .delete()
            .eq("user_id", user_id)
            .execute()
        )
        return True, ""
    except Exception as exc:
        return False, _friendly_db_error(str(exc))


def upsert_subscriptions_bulk(user_id: str, subs_list: List[Dict], access_token: str) -> Tuple[bool, str]:
    """
    Bulk-upsert a list of subscriptions for the authenticated user.
    Used when "Load Demo Dataset" is clicked — persists all demo records to the user's account.

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    client = _get_authed_client(access_token)
    if client is None:
        return False, "Database connection unavailable."

    if not subs_list:
        return True, ""

    try:
        rows = [_map_sub_dict_to_db_row(user_id, sub) for sub in subs_list]
        client.table("subscriptions").upsert(rows, on_conflict="id").execute()
        return True, ""
    except Exception as exc:
        return False, _friendly_db_error(str(exc))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_authed_client(access_token: str):
    """
    Return a Supabase client with the user's JWT set so RLS binds to auth.uid().
    Returns None if Supabase is not configured.
    """
    client = get_supabase_client()
    if client is None:
        return None

    if access_token:
        try:
            client.postgrest.auth(access_token)
        except Exception:
            pass

    return client


def _extract_user_dict(user, session) -> Dict[str, Any]:
    """
    Normalize a Supabase user + session object into a plain dict for session state.
    """
    metadata = {}
    try:
        metadata = user.user_metadata or {}
    except Exception:
        pass

    display_name = (
        metadata.get("display_name")
        or metadata.get("full_name")
        or metadata.get("name")
        or ""
    )

    access_token = ""
    try:
        if session:
            access_token = session.access_token or ""
    except Exception:
        pass

    return {
        "user_id": str(user.id),
        "email": str(user.email or ""),
        "display_name": str(display_name),
        "access_token": access_token,
    }


def _map_db_row_to_sub_dict(row: Dict) -> Dict:
    """
    Convert a Supabase subscriptions table row to the app's internal subscription dict format.
    """
    renewal = row.get("renewal_date") or ""
    created = row.get("created_at") or ""

    renewal = _normalize_date_str(renewal)
    created = _normalize_date_str(created)

    return {
        "id": str(row.get("id", "")),
        "service": str(row.get("name", "Unnamed Service")),
        "category": str(row.get("category", "Other")),
        "price": float(row.get("price", 0.0)),
        "currency": str(row.get("currency", "INR (₹)")),
        "billing_cycle": str(row.get("billing_cycle", "Monthly")),
        "renewal_date": renewal,
        "status": str(row.get("status", "Active")),
        "created_at": created,
    }


def _map_sub_dict_to_db_row(user_id: str, sub: Dict) -> Dict:
    """
    Convert the app's internal subscription dict to a Supabase table row.
    """
    renewal = _normalize_date_str(str(sub.get("renewal_date", "")))
    created = _normalize_date_str(str(sub.get("created_at", "")))
    if not created:
        created = date.today().isoformat()

    return {
        "id": str(sub.get("id", "")),
        "user_id": str(user_id),
        "name": str(sub.get("service", "Unnamed Service")),
        "price": float(sub.get("price", 0.0)),
        "billing_cycle": str(sub.get("billing_cycle", "Monthly")),
        "category": str(sub.get("category", "Other")),
        "currency": str(sub.get("currency", "INR (₹)")),
        "renewal_date": renewal if renewal else date.today().isoformat(),
        "status": str(sub.get("status", "Active")),
        "created_at": created,
    }


def _normalize_date_str(value: str) -> str:
    """
    Extract YYYY-MM-DD from a date or datetime string.
    Returns today's date string if parsing fails.
    """
    if not value:
        return date.today().isoformat()
    try:
        if len(value) == 10 and value[4] == "-":
            return value
        parsed = datetime.fromisoformat(value[:19])
        return parsed.strftime("%Y-%m-%d")
    except Exception:
        return date.today().isoformat()


def _friendly_auth_error(raw: str, include_raw: bool = False) -> str:
    """
    Map raw Supabase auth error strings to user-friendly messages.

    When include_raw=True the real error is appended in parentheses so
    misconfigurations or paused project states are visible without exposing secrets.
    """
    r = raw.lower()

    def _msg(friendly: str) -> str:
        if include_raw:
            return f"{friendly} (Supabase: {raw})"
        return friendly

    # Hostname / DNS / Connection failures (e.g. project paused, invalid URL ref, network down)
    if (
        "name or service not known" in r
        or "getaddrinfo failed" in r
        or "failed to establish" in r
        or "connection refused" in r
        or "max retries exceeded" in r
        or "nodename nor servname" in r
        or "cannot resolve" in r
    ):
        return _msg(
            "Cannot connect to Supabase host. "
            "Please check: (1) If your Supabase free-tier project is PAUSED due to inactivity, "
            "log in to Supabase Dashboard and click 'Restore project'; "
            "(2) Verify that SUPABASE_URL in Streamlit Cloud Secrets exactly matches your project URL."
        )

    # Timeouts
    if "timeout" in r or "timed out" in r:
        return _msg("Connection to Supabase timed out. Please check your internet connection and try again.")

    # Wrong email / password
    if "invalid login credentials" in r or "invalid credentials" in r:
        return _msg("Invalid email or password. Please try again.")

    # Email already registered
    if "user already registered" in r or "already been registered" in r or "already exists" in r:
        return _msg("An account with this email already exists. Please log in instead.")

    # Email confirmation required
    if "email not confirmed" in r:
        return _msg("Please confirm your email address before logging in. Check your inbox.")

    # Weak password
    if "password" in r and ("short" in r or "weak" in r or "length" in r or "characters" in r):
        return _msg("Password must be at least 6 characters long.")

    # Rate limiting
    if "rate limit" in r or "too many" in r or "429" in r:
        return _msg("Too many attempts. Please wait a moment and try again.")

    # Generic network
    if "network" in r or "connection" in r:
        return _msg("Network error. Please check your connection and try again.")

    # Catch-all
    return _msg(f"Authentication error: {raw}")


def _friendly_db_error(raw: str) -> str:
    """Map raw Supabase DB error strings to user-friendly messages."""
    r = raw.lower()
    if "jwt" in r or "token" in r or "unauthorized" in r or "401" in r:
        return "Your session has expired. Please log in again."
    if "network" in r or "connection" in r or "timeout" in r or "name or service not known" in r or "getaddrinfo" in r:
        return "Database connection error. Your Supabase project may be paused or unreachable."
    if "duplicate" in r or "unique" in r or "already exists" in r:
        return "This record already exists."
    return "A database error occurred. Please try again."
