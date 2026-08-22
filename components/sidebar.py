"""
Sidebar navigation and status component for SubSight AI.
Premium SaaS / Fintech Design System.
"""

import os
import streamlit as st
from services.analytics import get_demo_subscriptions
from services.gemini_service import verify_gemini_client
from services import supabase_service

from utils.config import GITHUB_REPO_URL

def render_sidebar() -> str:
    """
    Render the main sidebar navigation and return selected page name.
    """
    with st.sidebar:
        # Brand Header
        st.markdown(
            """
            <div style="padding: 12px 0 16px 0; border-bottom: 1px solid #F1F5F9; margin-bottom: 16px;">
                <div style="font-size: 18px; font-weight: 800; color: #0F172A; letter-spacing: -0.4px; display: flex; align-items: center; gap: 4px;">
                    <span>SUBSIGHT</span><span style="color: #2563EB;">.AI</span>
                </div>
                <div style="font-size: 11px; font-weight: 500; color: #64748B; margin-top: 2px; letter-spacing: 0.2px;">
                    Subscription Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Account Section (only shown when authenticated) ───────────────────
        is_authenticated = st.session_state.get("authenticated", False)

        if is_authenticated:
            user_email = st.session_state.get("user_email", "")
            user_name = st.session_state.get("user_display_name", "")
            display_label = user_name if user_name else (user_email.split("@")[0] if user_email else "User")
            initial = (user_name[0] if user_name else (user_email[0] if user_email else "U")).upper()

            st.markdown(
                """
                <div style="font-size: 10px; font-weight: 700; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">
                    ACCOUNT
                </div>
                """,
                unsafe_allow_html=True
            )

            # User badge
            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
                            padding: 8px 10px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px;">
                    <div style="width: 28px; height: 28px; background: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #2563EB; flex-shrink: 0;">
                        {initial}
                    </div>
                    <div style="min-width: 0; overflow: hidden;">
                        <div style="font-size: 12px; font-weight: 600; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.3;">
                            {display_label}
                        </div>
                        <div style="font-size: 10px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {user_email}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Log Out", use_container_width=True, key="sidebar_logout_btn"):
                _perform_logout()

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Navigation Options with Categories
        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">
                MAIN
            </div>
            """,
            unsafe_allow_html=True
        )

        nav_main = [
            "Dashboard",
            "Subscriptions",
            "AI Audit",
            "Savings Simulator",
            "Insights"
        ]

        nav_workspace = [
            "About"
        ]

        if "selected_page" not in st.session_state:
            st.session_state["selected_page"] = "Dashboard"

        current_sel = st.session_state.get("selected_page", "Dashboard")

        # Main section radio
        main_index = nav_main.index(current_sel) if current_sel in nav_main else 0
        selected_main = st.radio(
            "Main Navigation",
            options=nav_main,
            index=main_index,
            key="nav_radio_main",
            label_visibility="collapsed"
        )

        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase; margin-top: 14px; margin-bottom: 6px;">
                WORKSPACE
            </div>
            """,
            unsafe_allow_html=True
        )

        workspace_index = nav_workspace.index(current_sel) if current_sel in nav_workspace else None

        # Radio selection handler logic
        selected_workspace = None
        if current_sel in nav_workspace:
            selected_workspace = st.radio(
                "Workspace Navigation",
                options=nav_workspace,
                index=0,
                key="nav_radio_workspace",
                label_visibility="collapsed"
            )
        else:
            if st.button("About & Architecture", use_container_width=True, key="btn_nav_about"):
                st.session_state["selected_page"] = "About"
                st.rerun()

        # Update selected page state
        if selected_workspace:
            st.session_state["selected_page"] = selected_workspace
        else:
            st.session_state["selected_page"] = selected_main

        selected_page = st.session_state["selected_page"]

        st.markdown("<div style='height: 6px; border-bottom: 1px solid #F1F5F9; margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        # AI Engine Status Badge
        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">
                AI ENGINE
            </div>
            """,
            unsafe_allow_html=True
        )

        is_connected, _, status_text = verify_gemini_client()

        if is_connected:
            st.markdown(
                """
                <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 7px 10px; border-radius: 6px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="height: 7px; width: 7px; background-color: #059669; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 11px; font-weight: 600; color: #065F46;">Connected</span>
                    </div>
                    <span style="font-size: 9px; font-weight: 700; color: #047857; background: #DCFCE7; padding: 2px 6px; border-radius: 10px;">Gemini 2.5</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 7px 10px; border-radius: 6px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="height: 7px; width: 7px; background-color: #DC2626; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 11px; font-weight: 600; color: #991B1B;">Not Configured</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("Configure Key", expanded=False):
                custom_key = st.text_input(
                    "Gemini API Key",
                    type="password",
                    value=st.session_state.get("custom_api_key", ""),
                    help="Enter your Google Gemini API key"
                )
                if st.button("Save Key", use_container_width=True):
                    st.session_state["custom_api_key"] = custom_key.strip()
                    st.toast("Saved Gemini API Key!", icon="🔑")
                    st.rerun()

        st.markdown("<div style='height: 6px; border-bottom: 1px solid #F1F5F9; margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        # Compact Demo Data & Clear State Section with Confirmations
        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;">
                DEMO DATA
            </div>
            """,
            unsafe_allow_html=True
        )

        current_subs = st.session_state.get("subscriptions", [])
        has_subs = len(current_subs) > 0
        has_demo = (len(current_subs) == 8 and any(s.get("service") == "Netflix Premium" for s in current_subs))

        if has_demo:
            st.markdown(
                """
                <div style="font-size: 11px; color: #065F46; background: #F0FDF4; border: 1px solid #BBF7D0; padding: 8px 10px; border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-weight: 700;">✓ Demo Dataset Active</div>
                    <div style="font-size: 10px; color: #16A34A; margin-top: 2px;">8 sample subscriptions loaded.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if not st.session_state.get("confirm_clear_prompt"):
                if st.button("Clear Demo Data", use_container_width=True):
                    st.session_state["confirm_clear_prompt"] = True
                    st.rerun()
            else:
                st.warning("Remove all sample subscriptions?")
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    if st.button("Confirm", type="primary", use_container_width=True):
                        _clear_all_data()
                        st.session_state["confirm_clear_prompt"] = False
                        st.toast("Cleared demo subscriptions.", icon="🗑️")
                        st.rerun()
                with c_col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state["confirm_clear_prompt"] = False
                        st.rerun()
        else:
            st.markdown(
                """
                <div style="font-size: 11px; color: #64748B; margin-bottom: 8px; line-height: 1.4;">
                    Explore SubSight AI with realistic sample data.
                </div>
                """,
                unsafe_allow_html=True
            )

            if not st.session_state.get("confirm_load_prompt"):
                if st.button("Load Demo Dataset", use_container_width=True):
                    if has_subs:
                        st.session_state["confirm_load_prompt"] = True
                        st.rerun()
                    else:
                        _load_demo_data()
                        st.toast("Loaded demo subscription dataset!", icon="🚀")
                        st.rerun()
            else:
                st.warning("Replace current subscriptions with demo data?")
                l_col1, l_col2 = st.columns(2)
                with l_col1:
                    if st.button("Load", type="primary", use_container_width=True):
                        _load_demo_data()
                        st.session_state["confirm_load_prompt"] = False
                        st.toast("Loaded demo subscriptions!", icon="🚀")
                        st.rerun()
                with l_col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state["confirm_load_prompt"] = False
                        st.rerun()

        # Destructive Clear All Data option if user has custom data
        if has_subs and not has_demo:
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            if not st.session_state.get("confirm_clear_user_prompt"):
                if st.button("Clear Portfolio Data", use_container_width=True):
                    st.session_state["confirm_clear_user_prompt"] = True
                    st.rerun()
            else:
                st.warning("Remove all custom subscriptions?")
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    if st.button("Clear All", type="primary", use_container_width=True):
                        _clear_all_data()
                        st.session_state["confirm_clear_user_prompt"] = False
                        st.toast("Cleared all subscriptions.", icon="🗑️")
                        st.rerun()
                with u_col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state["confirm_clear_user_prompt"] = False
                        st.rerun()

        # Sidebar Footer
        st.markdown(
            f"""
            <div style="font-size: 11px; color: #94A3B8; padding-top: 16px; border-top: 1px solid #F1F5F9; margin-top: 20px;">
                <div style="font-weight: 700; color: #475569;">SubSight AI · v2.0</div>
                <div style="color: #94A3B8; font-size: 10px; margin-bottom: 6px;">Subscription Intelligence</div>
                <a href="{GITHUB_REPO_URL}" target="_blank" style="color: #2563EB; text-decoration: none; font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
                    <span>↗</span> View on GitHub
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    return selected_page


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _perform_logout() -> None:
    """
    Sign out of Supabase, clear all auth and subscription session state,
    and trigger a rerun to return to the auth screen.
    """
    access_token = st.session_state.get("access_token", "")
    supabase_service.sign_out(access_token)

    # Clear auth state
    for key in ["authenticated", "user_id", "user_email", "user_display_name", "access_token", "subscriptions_loaded"]:
        st.session_state.pop(key, None)

    # Clear data state
    st.session_state["subscriptions"] = []
    st.session_state["audit_result"] = None
    st.session_state["sim_audit_result"] = None
    st.session_state["audit_timestamp"] = None

    st.toast("Logged out successfully.", icon="👋")
    st.rerun()


def _load_demo_data() -> None:
    """
    Load demo subscriptions into session state AND persist them to Supabase
    for the authenticated user.
    """
    demo_subs = get_demo_subscriptions()
    st.session_state["subscriptions"] = demo_subs
    st.session_state["audit_result"] = None

    # Persist to Supabase if authenticated
    if st.session_state.get("authenticated"):
        user_id = st.session_state.get("user_id", "")
        access_token = st.session_state.get("access_token", "")
        if user_id and access_token:
            # Clear existing first, then insert demo data fresh
            supabase_service.delete_all_user_subscriptions(user_id, access_token)
            success, err = supabase_service.upsert_subscriptions_bulk(user_id, demo_subs, access_token)
            if not success:
                st.toast(f"Warning: Could not save demo data to database: {err}", icon="⚠️")


def _clear_all_data() -> None:
    """
    Clear all subscriptions from session state AND delete them from Supabase
    for the authenticated user.
    """
    # Clear Supabase first
    if st.session_state.get("authenticated"):
        user_id = st.session_state.get("user_id", "")
        access_token = st.session_state.get("access_token", "")
        if user_id and access_token:
            success, err = supabase_service.delete_all_user_subscriptions(user_id, access_token)
            if not success:
                st.toast(f"Warning: Could not delete from database: {err}", icon="⚠️")

    # Always clear session state regardless of DB result
    st.session_state["subscriptions"] = []
    st.session_state["audit_result"] = None
    st.session_state["sim_audit_result"] = None
    st.session_state["audit_timestamp"] = None
