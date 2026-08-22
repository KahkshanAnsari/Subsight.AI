"""
SubSight AI - Subscription Intelligence Platform
Premium Fintech / SaaS Design System · Version 2.0
"""

import datetime
from typing import Dict, Any, List
import pandas as pd
import streamlit as st

# Page Configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="SubSight AI — Subscription Intelligence",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Commercial Fintech / SaaS Aesthetics (Linear/Stripe-inspired)
st.markdown(
    """
    <style>
    /* Google Fonts Inter Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Main Application Background & Global Typography */
    html, body, .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #0F172A;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 6px;
    }
    
    /* Radio Button Navigation Polish */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 7px 12px !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        margin-bottom: 2px !important;
        transition: all 0.12s ease-in-out;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
        font-weight: 600 !important;
    }
    
    /* Page Hero Header Container */
    .page-hero {
        background: transparent;
        padding: 4px 0 20px 0;
        margin-bottom: 22px;
        border-bottom: 1px solid #E2E8F0;
    }
    .page-eyebrow {
        font-size: 11px;
        font-weight: 700;
        color: #2563EB;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .page-title {
        color: #0F172A;
        font-size: 26px;
        font-weight: 800;
        margin: 0 0 4px 0;
        letter-spacing: -0.5px;
        line-height: 1.25;
    }
    .page-subtitle {
        color: #64748B;
        font-size: 13.5px;
        margin: 0;
        font-weight: 400;
    }
    
    /* Streamlit Metric Styling Overrides */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        padding: 16px 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    [data-testid="stMetricDelta"] {
        font-size: 11px !important;
        font-weight: 500 !important;
    }
    
    /* Card Containers */
    .saas-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 22px 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    
    /* Button Hierarchy - Rock-solid contrast */
    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        transition: all 0.15s ease-in-out !important;
    }
    /* Primary Button */
    .stButton button[kind="primary"],
    .stButton button[data-testid="stBaseButton-primary"],
    div[data-testid="stFormSubmitButton"] button,
    button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2) !important;
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
        background: transparent !important;
    }
    .stButton button[kind="primary"]:hover,
    [data-testid="stBaseButton-primary"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28) !important;
    }
    .stButton button[kind="primary"]:hover *,
    [data-testid="stBaseButton-primary"]:hover *,
    div[data-testid="stFormSubmitButton"] button:hover * {
        color: #FFFFFF !important;
        background: transparent !important;
    }
    .stButton button[kind="primary"]:active,
    [data-testid="stBaseButton-primary"]:active,
    div[data-testid="stFormSubmitButton"] button:active {
        background-color: #1E40AF !important;
        border-color: #1E40AF !important;
    }
    .stButton button[kind="primary"]:active *,
    [data-testid="stBaseButton-primary"]:active *,
    div[data-testid="stFormSubmitButton"] button:active * {
        color: #FFFFFF !important;
        background: transparent !important;
    }
    /* Secondary Button */
    .stButton button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #94A3B8 !important;
    }
    
    /* Tabs styling */
    [data-testid="stTabs"] button {
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #64748B !important;
        padding: 8px 16px !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #2563EB !important;
        border-bottom-color: #2563EB !important;
    }
    
    /* Form inputs polish */
    div[data-baseweb="input"] {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }
    div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border-color: #CBD5E1 !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }
    
    /* Hide Default Footer */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Modular Package Imports
from utils.validators import (
    CATEGORIES, BILLING_CYCLES, STATUSES, CURRENCIES, 
    validate_price, validate_date_string, sanitize_subscription, generate_sub_id
)
from utils.calculations import (
    enrich_subscription_dataframe, calculate_portfolio_metrics, simulate_cancellation_scenario
)
from services.analytics import (
    get_demo_subscriptions, get_upcoming_renewals, get_category_breakdown
)
from services.gemini_service import run_ai_audit, run_savings_scenario_analysis, verify_gemini_client
from services import supabase_service
from utils.config import GITHUB_REPO_URL
from components.sidebar import render_sidebar
from components.auth_ui import render_auth_screen
from components.cards import (
    render_kpi_cards, render_ai_snapshot_card, render_upcoming_renewal_cards
)
from components.charts import (
    render_spending_overview_chart, render_category_donut_chart, 
    render_simulator_comparison_chart, render_top_expensive_chart, 
    render_billing_cycle_chart, render_renewal_timeline_chart
)
from components.tables import (
    render_dashboard_subscription_table, render_editable_subscriptions_table, filter_subscriptions
)


# ==============================================================================
# AUTHENTICATION — Session State Initialization
# ==============================================================================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = ""
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "user_display_name" not in st.session_state:
    st.session_state["user_display_name"] = ""
if "access_token" not in st.session_state:
    st.session_state["access_token"] = ""
if "subscriptions_loaded" not in st.session_state:
    st.session_state["subscriptions_loaded"] = False


# ==============================================================================
# AUTHENTICATION GUARD
# ==============================================================================

if not st.session_state["authenticated"]:
    render_auth_screen()
    st.stop()  # Halt execution for unauthenticated requests


# ==============================================================================
# SUBSCRIPTION LOADING (once per session, after login)
# ==============================================================================

if not st.session_state["subscriptions_loaded"]:
    user_id = st.session_state["user_id"]
    access_token = st.session_state["access_token"]
    
    if user_id and access_token and supabase_service.is_supabase_configured():
        success, subs, err = supabase_service.get_user_subscriptions(user_id, access_token)
        if success:
            st.session_state["subscriptions"] = subs
        else:
            if "session has expired" in err.lower() or "jwt" in err.lower():
                for k in ["authenticated", "user_id", "user_email", "user_display_name", "access_token", "subscriptions_loaded"]:
                    st.session_state.pop(k, None)
                st.session_state["subscriptions"] = []
                st.warning("Your session has expired. Please log in again.")
                st.rerun()
            else:
                st.session_state["subscriptions"] = []
                st.warning(f"⚠️ Could not load subscriptions from database: {err}")
    else:
        if "subscriptions" not in st.session_state:
            st.session_state["subscriptions"] = []

    st.session_state["subscriptions_loaded"] = True


# ==============================================================================
# Safe Session State Initialization (non-auth keys)
# ==============================================================================

if "subscriptions" not in st.session_state:
    st.session_state["subscriptions"] = []

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Dashboard"

if "audit_result" not in st.session_state:
    st.session_state["audit_result"] = None

if "audit_timestamp" not in st.session_state:
    st.session_state["audit_timestamp"] = None

if "sim_audit_result" not in st.session_state:
    st.session_state["sim_audit_result"] = None


# ==============================================================================
# SUPABASE HELPERS — CRUD operations
# ==============================================================================

def _db_insert(sub_dict: dict) -> None:
    """Persist a new subscription to Supabase."""
    if st.session_state.get("authenticated") and supabase_service.is_supabase_configured():
        uid = st.session_state.get("user_id", "")
        tok = st.session_state.get("access_token", "")
        if uid and tok:
            success, err = supabase_service.insert_subscription(uid, sub_dict, tok)
            if not success:
                st.toast(f"⚠️ Subscription saved locally but not to database: {err}", icon="⚠️")


def _db_upsert(sub_dict: dict) -> None:
    """Upsert a subscription to Supabase."""
    if st.session_state.get("authenticated") and supabase_service.is_supabase_configured():
        uid = st.session_state.get("user_id", "")
        tok = st.session_state.get("access_token", "")
        if uid and tok:
            success, err = supabase_service.upsert_subscription(uid, sub_dict, tok)
            if not success:
                st.toast(f"⚠️ Could not sync to database: {err}", icon="⚠️")


def _db_delete(sub_id: str) -> None:
    """Delete a subscription from Supabase."""
    if st.session_state.get("authenticated") and supabase_service.is_supabase_configured():
        uid = st.session_state.get("user_id", "")
        tok = st.session_state.get("access_token", "")
        if uid and tok:
            success, err = supabase_service.delete_subscription(uid, sub_id, tok)
            if not success:
                st.toast(f"⚠️ Could not delete from database: {err}", icon="⚠️")


# Render Sidebar Navigation
current_page = render_sidebar()

# Convert Session State Subscriptions list to Pandas DataFrame
raw_subs = st.session_state.get("subscriptions", [])
df_subs = pd.DataFrame(raw_subs) if raw_subs else pd.DataFrame()
df_enriched = enrich_subscription_dataframe(df_subs)
portfolio_metrics = calculate_portfolio_metrics(df_subs)
has_demo = len(raw_subs) == 8 and any(s.get("service") == "Netflix Premium" for s in raw_subs)


# ==============================================================================
# PAGE 1: DASHBOARD
# ==============================================================================
if current_page == "Dashboard":
    # Dynamic personalized greeting
    hour = datetime.datetime.now().hour
    time_greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")
    user_name = st.session_state.get("user_display_name", "")
    user_email = st.session_state.get("user_email", "")
    display_greeting_name = user_name.split()[0] if user_name else (user_email.split("@")[0] if user_email else "there")

    st.markdown(
        f"""
        <div class="page-hero">
            <div class="page-eyebrow">Subscription Overview</div>
            <h1 class="page-title">{time_greeting}, {display_greeting_name}</h1>
            <p class="page-subtitle">Here's what your subscription portfolio looks like today.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # KPI Metrics Row
    render_kpi_cards(portfolio_metrics, has_demo_data=has_demo)
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Overview Charts Row
    col_chart1, col_chart2 = st.columns([1.6, 1])
    
    with col_chart1:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        view_mode = st.radio(
            "Spending View Cycle",
            options=["Monthly", "Annual"],
            horizontal=True,
            key="dash_view_mode"
        )
        render_spending_overview_chart(df_subs, view_type=view_mode)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        render_category_donut_chart(df_subs)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Table & Alerts Row
    col_tb, col_side = st.columns([1.6, 1])
    
    with col_tb:
        st.markdown("### Active Subscription Summary")
        render_dashboard_subscription_table(df_subs)
        
    with col_side:
        st.markdown("### Upcoming Renewals (30 Days)")
        upcoming = get_upcoming_renewals(df_subs, days_ahead=30)
        render_upcoming_renewal_cards(upcoming)
        
        # AI Snapshot Card
        render_ai_snapshot_card(
            st.session_state.get("audit_result"),
            on_run_audit_cb=None
        )


# ==============================================================================
# PAGE 2: SUBSCRIPTIONS (CRUD Management & st.data_editor)
# ==============================================================================
elif current_page == "Subscriptions":
    st.markdown(
        """
        <div class="page-hero">
            <div class="page-eyebrow">Portfolio Management</div>
            <h1 class="page-title">Manage Subscriptions</h1>
            <p class="page-subtitle">Add, update, filter, and track all your recurring commitments.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Add Subscription Form Expander
    with st.expander("➕ Add New Subscription", expanded=False):
        with st.form("add_sub_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                form_service = st.text_input("Service Name*", placeholder="e.g. Netflix, GitHub, ChatGPT")
                form_category = st.selectbox("Category*", options=CATEGORIES, index=0)
            with f_col2:
                form_price = st.number_input("Price*", min_value=0.0, step=10.0, value=299.0, format="%.2f")
                form_currency = st.selectbox("Currency*", options=list(CURRENCIES.keys()), index=0)
            with f_col3:
                form_cycle = st.selectbox("Billing Cycle*", options=BILLING_CYCLES, index=0)
                form_date = st.date_input("Next Renewal Date*", value=datetime.date.today() + datetime.timedelta(days=30))
                
            form_status = st.selectbox("Status*", options=STATUSES, index=0)
            
            submit_btn = st.form_submit_button("Save Subscription", type="primary", use_container_width=True)
            
            if submit_btn:
                if not form_service.strip():
                    st.error("Service Name cannot be empty.")
                elif form_price <= 0:
                    st.error("Price must be greater than 0.")
                else:
                    new_sub = sanitize_subscription({
                        "id": generate_sub_id(),
                        "service": form_service,
                        "category": form_category,
                        "price": form_price,
                        "currency": form_currency,
                        "billing_cycle": form_cycle,
                        "renewal_date": form_date.strftime("%Y-%m-%d"),
                        "status": form_status
                    })
                    st.session_state["subscriptions"].append(new_sub)
                    _db_insert(new_sub)
                    st.success(f"Added subscription '{form_service}' successfully!")
                    st.rerun()

    # Search & Filter Controls
    f_c1, f_c2, f_c3 = st.columns([1.5, 1, 1])
    with f_c1:
        search_q = st.text_input("🔍 Search Service", placeholder="Type to search...", key="sub_search")
    with f_c2:
        cat_filter = st.selectbox("Filter Category", options=["All Categories"] + CATEGORIES, key="sub_cat_filter")
    with f_c3:
        status_filter = st.selectbox("Filter Status", options=["All Statuses"] + STATUSES, key="sub_status_filter")
        
    filtered_df = filter_subscriptions(df_enriched, search_q, cat_filter, status_filter)
    
    st.markdown("### Interactive Subscriptions Editor")
    st.caption("Edits made in the table below automatically save to your workspace.")
    
    if not filtered_df.empty:
        edited_df = render_editable_subscriptions_table(filtered_df)
        
        # Auto-sync session state if table edits occurred
        if edited_df is not None and not edited_df.empty:
            curr_map = {s["id"]: s for s in st.session_state["subscriptions"]}
            has_changes = False
            changed_subs = []
            
            for _, r in edited_df.iterrows():
                sub_dict = sanitize_subscription(r.to_dict())
                sid = sub_dict["id"]
                if sid not in curr_map or curr_map[sid] != sub_dict:
                    curr_map[sid] = sub_dict
                    has_changes = True
                    changed_subs.append(sub_dict)
                    
            if has_changes:
                st.session_state["subscriptions"] = list(curr_map.values())
                for changed_sub in changed_subs:
                    _db_upsert(changed_sub)
                st.toast("Subscriptions synchronized!", icon="💾")
        
        # Action controls bar
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            if st.button("💾 Sync State", type="primary", use_container_width=True):
                st.success("Session state synchronized!")
                st.rerun()
                
        with col_btn2:
            csv_data = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name="subsight_subscriptions.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with col_btn3:
            sub_options = {f"{r['service']} ({r['id']})": r["id"] for _, r in filtered_df.iterrows()}
            selected_to_del = st.selectbox("Select Subscription to Delete", options=["None"] + list(sub_options.keys()))
            if selected_to_del != "None":
                del_id = sub_options[selected_to_del]
                if st.button(f"🗑️ Delete {selected_to_del.split(' (')[0]}", use_container_width=True):
                    st.session_state["subscriptions"] = [
                        s for s in st.session_state["subscriptions"] if s["id"] != del_id
                    ]
                    _db_delete(del_id)
                    st.toast("Subscription deleted.", icon="🗑️")
                    st.rerun()
    else:
        st.info("No subscriptions match your search/filter criteria.")


# ==============================================================================
# PAGE 3: AI AUDIT
# ==============================================================================
elif current_page == "AI Audit":
    st.markdown(
        """
        <div class="page-hero">
            <div class="page-eyebrow" style="color: #7C3AED;">AI Intelligence</div>
            <h1 class="page-title">AI Subscription Audit</h1>
            <p class="page-subtitle">Your portfolio, analyzed intelligently by Google Gemini.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    is_connected, _, status_msg = verify_gemini_client()
    
    if not is_connected:
        st.warning(
            f"⚠️ Gemini API Key is required to run the AI Audit. Current status: {status_msg}. "
            "Please configure your key in the sidebar."
        )
        
    col_audit_btn, col_audit_status = st.columns([1, 2])
    with col_audit_btn:
        run_audit_now = st.button("🤖 Generate AI Audit", type="primary", use_container_width=True)
        
    if run_audit_now:
        if df_subs.empty:
            st.error("Please add subscriptions or load demo data before running the AI Audit.")
        else:
            with st.spinner("Analyzing portfolio with Google Gemini AI..."):
                success, result = run_ai_audit(df_subs)
                if success:
                    st.session_state["audit_result"] = result
                    st.session_state["audit_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("AI Subscription Audit generated successfully!")
                else:
                    st.error(f"Audit Generation Failed: {result}")
                    
    # Display Audit Output
    audit_data = st.session_state.get("audit_result")
    audit_ts = st.session_state.get("audit_timestamp")
    
    if audit_data:
        st.markdown(
            f"""
            <div style="background: #F5F3FF; border: 1px solid #DDD6FE; padding: 10px 16px; border-radius: 8px; margin-bottom: 20px; font-size: 12px; color: #5B21B6; display: flex; align-items: center; justify-content: space-between;">
                <span><strong>Audit Generated:</strong> {audit_ts}</span>
                <span style="font-weight: 700; color: #7C3AED; background: #EDE9FE; padding: 2px 8px; border-radius: 10px;">GEMINI 2.5 ENGINE</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown(audit_data)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.download_button(
            label="📄 Download Audit Report (.md)",
            data=f"# SubSight AI Audit Report\nGenerated on: {audit_ts}\n\n{audit_data}",
            file_name=f"SubSight_AI_Audit_{datetime.date.today()}.md",
            mime="text/markdown"
        )
    else:
        st.info("Click **'Generate AI Audit'** above to run an intelligent analysis on your current subscriptions.")


# ==============================================================================
# PAGE 4: SAVINGS SIMULATOR
# ==============================================================================
elif current_page == "Savings Simulator":
    st.markdown(
        """
        <div class="page-hero">
            <div class="page-eyebrow">Financial Optimization</div>
            <h1 class="page-title">Savings Simulator</h1>
            <p class="page-subtitle">Simulate subscription cancellation scenarios and calculate instant financial impact.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if df_subs.empty:
        st.info("Please add subscriptions or load demo data to use the simulator.")
    else:
        enriched_active = df_enriched[df_enriched["status"].isin(["Active", "Review Needed"])]
        
        st.markdown("### Select Subscriptions to Simulate Cancelling")
        
        sub_select_map = {
            f"{r['service']} — ₹{r['monthly_cost']:,.2f}/mo ({r['category']})": r["id"]
            for _, r in enriched_active.iterrows()
        }
        
        selected_labels = st.multiselect(
            "Choose subscriptions to remove from portfolio:",
            options=list(sub_select_map.keys()),
            default=[k for k, v in sub_select_map.items() if "Review Needed" in k]
        )
        
        selected_cancel_ids = [sub_select_map[lbl] for lbl in selected_labels]
        
        sim_res = simulate_cancellation_scenario(df_subs, selected_cancel_ids)
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Simulation Result KPI Cards
        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        with m_c1:
            st.metric("Current Spend", f"₹{sim_res['current_monthly']:,.2f}/mo")
        with m_c2:
            st.metric("Optimized Spend", f"₹{sim_res['new_monthly']:,.2f}/mo")
        with m_c3:
            st.metric("Monthly Savings", f"₹{sim_res['monthly_savings']:,.2f}", delta=f"-{sim_res['savings_percentage']:.1f}%", delta_color="normal")
        with m_c4:
            st.metric("Projected Annual Savings", f"₹{sim_res['annual_savings']:,.2f}", delta=f"{sim_res['cancelled_count']} Cut", delta_color="normal")
            
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        
        col_sim_chart, col_sim_ai = st.columns([1.2, 1])
        
        with col_sim_chart:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            render_simulator_comparison_chart(sim_res)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_sim_ai:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            st.markdown("#### AI Scenario Impact Analysis")
            
            if st.button("🤖 Evaluate Scenario Trade-offs with AI", type="primary", use_container_width=True):
                with st.spinner("Analyzing trade-offs..."):
                    success, sim_ai_out = run_savings_scenario_analysis(df_subs, selected_cancel_ids, sim_res)
                    if success:
                        st.session_state["sim_audit_result"] = sim_ai_out
                    else:
                        st.error(sim_ai_out)
                        
            sim_ai_text = st.session_state.get("sim_audit_result")
            if sim_ai_text:
                st.markdown(f"<div style='font-size: 13px; color: #1E293B; line-height: 1.5;'>{sim_ai_text}</div>", unsafe_allow_html=True)
            else:
                st.caption("Select subscriptions above and click evaluate to get AI feedback on lost features vs savings.")
            st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 5: INSIGHTS & ANALYTICS
# ==============================================================================
elif current_page == "Insights":
    st.markdown(
        """
        <div class="page-hero">
            <div class="page-eyebrow">Expense Analytics</div>
            <h1 class="page-title">Portfolio Analytics & Insights</h1>
            <p class="page-subtitle">Deep-dive into expense distribution, top cost drivers, renewal timelines, and cycle splits.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if df_subs.empty:
        st.info("No data available for analytics. Add subscriptions or load demo data.")
    else:
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            render_top_expensive_chart(df_subs)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with row1_col2:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            render_billing_cycle_chart(df_subs)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        render_renewal_timeline_chart(df_subs)
        st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("#### Category Distribution Breakdown")
        cat_analytics_df = get_category_breakdown(df_subs)
        st.dataframe(
            cat_analytics_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "category": st.column_config.TextColumn("Category", width="medium"),
                "monthly_cost": st.column_config.NumberColumn("Monthly Cost", format="₹%.2f"),
                "annual_cost": st.column_config.NumberColumn("Annual Projection", format="₹%.2f"),
                "count": st.column_config.NumberColumn("Count"),
                "share_pct": st.column_config.NumberColumn("Portfolio Share (%)", format="%.1f%%"),
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 6: ABOUT & SYSTEM DESIGN
# ==============================================================================
elif current_page == "About":
    st.markdown(
        """
        <div class="page-hero">
            <div class="page-eyebrow">System Architecture</div>
            <h1 class="page-title">SubSight AI</h1>
            <p class="page-subtitle">Understand your subscriptions. Cut the waste.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="saas-card">
            <h3 style="color: #0F172A; margin-top: 0; font-size: 16px; font-weight: 700;">Product Overview</h3>
            <p style="color: #475569; font-size: 13.5px; line-height: 1.6; margin-bottom: 0;">
                SubSight AI is a modern subscription intelligence platform designed to help individuals and teams track, analyze, and optimize recurring software and streaming commitments. 
                Using Google Gemini AI, it evaluates active subscriptions to detect redundant service pairs, quantify annual financial commitments, and generate actionable savings recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="saas-card">
            <h3 style="color: #0F172A; margin-top: 0; font-size: 16px; font-weight: 700; margin-bottom: 14px;">Technology Stack</h3>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span style="background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 16px;">Python 3.11+</span>
                <span style="background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 16px;">Streamlit</span>
                <span style="background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 16px;">Pandas</span>
                <span style="background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 16px;">Plotly</span>
                <span style="background: #F0FDF4; color: #16A34A; border: 1px solid #BBF7D0; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 16px;">Google Gemini AI</span>
                <span style="background: #F5F3FF; color: #7C3AED; border: 1px solid #DDD6FE; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 16px;">Supabase Auth & PostgreSQL</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_about_git, col_about_cap = st.columns(2)
    
    with col_about_git:
        st.markdown(
            f"""
            <div class="saas-card">
                <h3 style="color: #0F172A; margin-top: 0; font-size: 16px; font-weight: 700;">Open Source Repository</h3>
                <p style="color: #64748B; font-size: 13px; line-height: 1.5; margin-bottom: 16px;">
                    Explore the full source code, technical architecture, and system documentation on GitHub.
                </p>
                <a href="{GITHUB_REPO_URL}" target="_blank" style="background: #2563EB; color: #FFFFFF; font-weight: 600; font-size: 13px; padding: 8px 16px; border-radius: 6px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                    View on GitHub ↗
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_about_cap:
        st.markdown(
            """
            <div class="saas-card">
                <h3 style="color: #0F172A; margin-top: 0; font-size: 16px; font-weight: 700;">Capstone Project</h3>
                <p style="color: #64748B; font-size: 13px; line-height: 1.5; margin-bottom: 12px;">
                    Developed as a B.Tech Artificial Intelligence Capstone Project.
                </p>
                <div style="font-size: 12px; font-weight: 600; color: #0F172A; background: #F8FAFC; padding: 8px 12px; border-radius: 6px; border: 1px solid #E2E8F0;">
                    B.Tech AI Capstone · Version 2.0
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
