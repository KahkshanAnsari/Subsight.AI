"""
Authentication UI component for SubSight AI.
Clean Commercial Fintech SaaS Design System.
"""

import textwrap
import streamlit as st
from services import supabase_service


def render_auth_screen() -> None:
    """
    Render the clean, two-column authentication screen.
    Preserves all Supabase Auth logic while providing a polished commercial UI.
    """

    # ── Targeted CSS for Pure White Buttons, Clean Inputs, and Card Containers ──
    css_content = textwrap.dedent("""
    <style>
    /* Container spacing */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1060px !important;
    }

    /* ── Form Card Container (Wraps the form in a crisp white card) ── */
    div[data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 26px 28px 24px 28px !important;
        box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06) !important;
    }

    /* ── CRITICAL: Primary Button Text Contrast (100% Pure White in all states) ── */
    .stButton button[kind="primary"],
    .stButton button[data-testid="stBaseButton-primary"],
    div[data-testid="stFormSubmitButton"] button,
    button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 48px !important;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stButton button[kind="primary"] *,
    .stButton button[kind="primary"] p,
    .stButton button[kind="primary"] span,
    .stButton button[kind="primary"] div,
    div[data-testid="stFormSubmitButton"] button *,
    div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stFormSubmitButton"] button span,
    div[data-testid="stFormSubmitButton"] button div,
    [data-testid="stBaseButton-primary"] *,
    [data-testid="stBaseButton-primary"] p,
    [data-testid="stBaseButton-primary"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        background: transparent !important;
    }

    /* Primary Button Hover */
    .stButton button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.28) !important;
    }
    .stButton button[kind="primary"]:hover *,
    [data-testid="stBaseButton-primary"]:hover *,
    div[data-testid="stFormSubmitButton"] button:hover * {
        color: #FFFFFF !important;
        background: transparent !important;
    }

    /* Primary Button Active */
    .stButton button[kind="primary"]:active,
    [data-testid="stBaseButton-primary"]:active,
    div[data-testid="stFormSubmitButton"] button:active {
        background-color: #1E40AF !important;
        border-color: #1E40AF !important;
        transform: translateY(1px) !important;
    }
    .stButton button[kind="primary"]:active *,
    [data-testid="stBaseButton-primary"]:active *,
    div[data-testid="stFormSubmitButton"] button:active * {
        color: #FFFFFF !important;
        background: transparent !important;
    }

    /* ── Form Inputs ── */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        min-height: 46px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-baseweb="input"]:hover {
        border-color: #94A3B8 !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }
    div[data-baseweb="input"] > div {
        background-color: transparent !important;
        padding: 0 4px !important;
    }
    div[data-baseweb="input"] input {
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 14px !important;
        padding: 10px 12px !important;
        background: transparent !important;
    }
    div[data-baseweb="input"] input::placeholder {
        color: #94A3B8 !important;
        font-size: 14px !important;
    }
    [data-testid="stTextInput"] label,
    [data-testid="stTextInput"] label p {
        color: #0F172A !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
        letter-spacing: -0.1px !important;
    }

    /* ── Tabs Styling ── */
    div[data-testid="stTabs"] {
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 18px !important;
    }
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 16px !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 4px !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        background: transparent !important;
        border-radius: 0 !important;
        transition: color 0.15s ease, border-color 0.15s ease !important;
    }
    div[data-testid="stTabs"] button[role="tab"] p,
    div[data-testid="stTabs"] button[role="tab"] span {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        border-bottom: 2px solid #2563EB !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] span {
        color: #2563EB !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="false"] p,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="false"] span {
        color: #64748B !important;
    }
    div[data-testid="stTabs"] button[role="tab"]:hover p,
    div[data-testid="stTabs"] button[role="tab"]:hover span {
        color: #0F172A !important;
    }

    /* ── Alert Styling ── */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    </style>
    """)
    st.markdown(css_content, unsafe_allow_html=True)

    # ── Supabase availability check ──────────────────────────────────────────
    _, _, _cred_err = supabase_service._load_credentials()
    if _cred_err:
        config_err_html = textwrap.dedent(f"""
        <div style="max-width: 580px; margin: 40px auto; padding: 28px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);">
            <div style="font-size: 18px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">
                SUBSIGHT<span style="color: #2563EB;">.AI</span>
            </div>
            <div style="font-size: 13px; font-weight: 600; color: #DC2626; margin-bottom: 12px;">
                ⚠️ Supabase Configuration Required
            </div>
            <div style="font-size: 13px; color: #475569; margin-bottom: 16px;">
                {_cred_err}
            </div>
        </div>
        """)
        st.markdown(config_err_html, unsafe_allow_html=True)
        with st.expander("Configuration Instructions", expanded=True):
            st.code(
                """# .streamlit/secrets.toml
GEMINI_API_KEY = "your-gemini-api-key"
SUPABASE_URL   = "https://your-project-ref.supabase.co"
SUPABASE_KEY   = "your-anon-public-key"
""",
                language="toml",
            )
            st.markdown(
                "Find your credentials in [Supabase Dashboard](https://supabase.com/dashboard) → **Project Settings** → **API**"
            )
        return

    # ── Main Two-Column Layout ───────────────────────────────────────────────
    col_left, col_right = st.columns([1.05, 0.95], gap="large")

    # ── Left Area: Clean Dark Navy Brand Panel ──────────────────────────────
    with col_left:
        left_panel_html = textwrap.dedent("""
        <div style="background: linear-gradient(165deg, #0F172A 0%, #172554 100%); border-radius: 18px; padding: 40px 34px; height: 100%; min-height: 480px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 12px 36px rgba(15, 23, 42, 0.12); border: 1px solid rgba(255, 255, 255, 0.08);">
            <div>
                <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 22px; display: flex; align-items: center; gap: 4px;">
                    <span>SUBSIGHT</span><span style="color: #60A5FA;">.AI</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255, 255, 255, 0.07); padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 18px;">
                    <span style="height: 6px; width: 6px; background-color: #38BDF8; border-radius: 50%; display: inline-block;"></span>
                    <span style="font-size: 10.5px; font-weight: 700; color: #93C5FD; letter-spacing: 0.8px; text-transform: uppercase;">SUBSCRIPTION INTELLIGENCE</span>
                </div>
                <div style="font-size: 24px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px; line-height: 1.25; margin-bottom: 12px;">
                    Take control of every subscription.
                </div>
                <div style="font-size: 13.5px; color: #94A3B8; line-height: 1.6; margin-bottom: 28px;">
                    Track recurring spending, uncover hidden waste, and make smarter subscription decisions with AI.
                </div>
                <div style="display: flex; flex-direction: column; gap: 15px;">
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                        <div style="width: 22px; height: 22px; border-radius: 6px; background: rgba(5, 150, 105, 0.15); border: 1px solid rgba(5, 150, 105, 0.3); display: flex; align-items: center; justify-content: center; color: #34D399; font-size: 12px; font-weight: 700; flex-shrink: 0; margin-top: 2px;">✓</div>
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #FFFFFF; line-height: 1.3;">Centralized Portfolio</div>
                            <div style="font-size: 11.5px; color: #94A3B8; margin-top: 2px;">Track renewal dates, billing cycles, and annual commitments.</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                        <div style="width: 22px; height: 22px; border-radius: 6px; background: rgba(124, 58, 237, 0.15); border: 1px solid rgba(124, 58, 237, 0.3); display: flex; align-items: center; justify-content: center; color: #C084FC; font-size: 12px; font-weight: 700; flex-shrink: 0; margin-top: 2px;">✓</div>
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #FFFFFF; line-height: 1.3;">AI Spending Audit</div>
                            <div style="font-size: 11.5px; color: #94A3B8; margin-top: 2px;">Detect redundant tiers and uncover savings with Gemini.</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                        <div style="width: 22px; height: 22px; border-radius: 6px; background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(37, 99, 235, 0.3); display: flex; align-items: center; justify-content: center; color: #60A5FA; font-size: 12px; font-weight: 700; flex-shrink: 0; margin-top: 2px;">✓</div>
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #FFFFFF; line-height: 1.3;">Zero-Knowledge Isolation</div>
                            <div style="font-size: 11.5px; color: #94A3B8; margin-top: 2px;">PostgreSQL Row Level Security keeps your data private.</div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="font-size: 11px; color: #64748B; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 28px;">
                🔒 Enterprise-grade Supabase Auth · Passwords never stored
            </div>
        </div>
        """)
        st.markdown(left_panel_html, unsafe_allow_html=True)

    # ── Right Area: Clean Heading & Authentication Form ──────────────────────
    with col_right:
        # Page Heading: Welcome to SUBSIGHT. AI
        heading_html = textwrap.dedent("""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 30px; font-weight: 700; color: #0F172A; letter-spacing: -0.6px; line-height: 1.2;">
                Welcome to SUBSIGHT<span style="color: #2563EB;">.AI</span>
            </div>
        </div>
        """)
        st.markdown(heading_html, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        # ── LOGIN TAB ────────────────────────────────────────────────────────
        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                tab_heading_html = textwrap.dedent("""
                <div style="margin-bottom: 16px;">
                    <div style="font-size: 18px; font-weight: 700; color: #0F172A; letter-spacing: -0.3px;">Welcome back</div>
                    <div style="font-size: 13px; color: #64748B; margin-top: 2px;">Enter your credentials to access your workspace.</div>
                </div>
                """)
                st.markdown(tab_heading_html, unsafe_allow_html=True)

                login_email = st.text_input(
                    "Email address",
                    placeholder="you@example.com",
                    key="login_email_input",
                )
                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="login_password_input",
                )
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                login_btn = st.form_submit_button(
                    "Sign In to Workspace",
                    type="primary",
                    use_container_width=True,
                )

            if login_btn:
                if not login_email.strip():
                    st.error("Please enter your email address.")
                elif not login_password:
                    st.error("Please enter your password.")
                else:
                    with st.spinner("Authenticating…"):
                        success, user_dict, err_msg = supabase_service.sign_in(
                            login_email, login_password
                        )
                    if success and user_dict:
                        _set_auth_state(user_dict)
                        st.success("Signed in successfully!")
                        st.rerun()
                    else:
                        st.error(f"{err_msg}")

        # ── SIGN UP TAB ──────────────────────────────────────────────────────
        with tab_signup:
            with st.form("signup_form", clear_on_submit=True):
                signup_heading_html = textwrap.dedent("""
                <div style="margin-bottom: 16px;">
                    <div style="font-size: 18px; font-weight: 700; color: #0F172A; letter-spacing: -0.3px;">Create your account</div>
                    <div style="font-size: 13px; color: #64748B; margin-top: 2px;">Get started with private subscription intelligence.</div>
                </div>
                """)
                st.markdown(signup_heading_html, unsafe_allow_html=True)

                signup_name = st.text_input(
                    "Full Name",
                    placeholder="e.g. Alex Morgan",
                    key="signup_name_input",
                )
                signup_email = st.text_input(
                    "Email address",
                    placeholder="you@example.com",
                    key="signup_email_input",
                )
                signup_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Minimum 6 characters",
                    key="signup_password_input",
                )
                signup_confirm = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter password",
                    key="signup_confirm_input",
                )
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                signup_btn = st.form_submit_button(
                    "Create Your Account",
                    type="primary",
                    use_container_width=True,
                )

            if signup_btn:
                errors = _validate_signup(
                    signup_name, signup_email, signup_password, signup_confirm
                )
                if errors:
                    for err in errors:
                        st.error(f"{err}")
                else:
                    with st.spinner("Creating account…"):
                        success, user_dict, err_msg = supabase_service.sign_up(
                            signup_email, signup_password, signup_name
                        )
                    if success and user_dict:
                        _set_auth_state(user_dict)
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.error(f"{err_msg}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _set_auth_state(user_dict: dict) -> None:
    """Populate all authentication-related session state keys."""
    st.session_state["authenticated"] = True
    st.session_state["user_id"] = user_dict.get("user_id", "")
    st.session_state["user_email"] = user_dict.get("email", "")
    st.session_state["user_display_name"] = user_dict.get("display_name", "")
    st.session_state["access_token"] = user_dict.get("access_token", "")
    st.session_state["subscriptions_loaded"] = False


def _validate_signup(name: str, email: str, password: str, confirm: str) -> list:
    """Return a list of validation error strings (empty list = valid)."""
    errors = []
    if not name.strip():
        errors.append("Full name is required.")
    if not email.strip():
        errors.append("Email address is required.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Please enter a valid email address.")
    if not password:
        errors.append("Password is required.")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters long.")
    if password != confirm:
        errors.append("Passwords do not match.")
    return errors
