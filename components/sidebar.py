"""
Sidebar navigation and status component for SubSight AI.
Follows clean SaaS design system with navigation grouping, status badges,
and confirmation UI for data modifications.
"""

import os
import streamlit as st
from services.analytics import get_demo_subscriptions
from services.gemini_service import verify_gemini_client

from utils.config import GITHUB_REPO_URL

def render_sidebar() -> str:
    """
    Render the main sidebar navigation and return selected page name.
    """
    with st.sidebar:
        # Brand Header
        st.markdown(
            """
            <div style="padding: 8px 0 16px 0;">
                <div style="font-size: 20px; font-weight: 800; color: #172554; letter-spacing: -0.5px; display: flex; align-items: center; gap: 4px;">
                    <span>SUBSIGHT</span><span style="color: #2563EB;">.AI</span>
                </div>
                <div style="font-size: 11px; font-weight: 500; color: #64748B; margin-top: 2px;">
                    Subscription Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        
        # Navigation Options with Categories
        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px;">
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
            <div style="font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.8px; text-transform: uppercase; margin-top: 14px; margin-bottom: 6px;">
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
            if st.button("ℹ️ About", use_container_width=True, key="btn_nav_about"):
                st.session_state["selected_page"] = "About"
                st.rerun()

        # Update selected page state
        if selected_workspace:
            st.session_state["selected_page"] = selected_workspace
        else:
            st.session_state["selected_page"] = selected_main
            
        selected_page = st.session_state["selected_page"]
        
        st.divider()
        
        # AI Engine Status Badge
        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px;">
                AI ENGINE STATUS
            </div>
            """,
            unsafe_allow_html=True
        )
        
        is_connected, _, status_text = verify_gemini_client()
        
        if is_connected:
            st.markdown(
                """
                <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 8px 12px; border-radius: 6px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="height: 8px; width: 8px; background-color: #16A34A; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 12px; font-weight: 600; color: #166534;">Connected</span>
                    </div>
                    <span style="font-size: 10px; font-weight: 600; color: #15803D; background: #DCFCE7; padding: 2px 6px; border-radius: 4px;">Gemini 2.5</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 8px 12px; border-radius: 6px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="height: 8px; width: 8px; background-color: #DC2626; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 12px; font-weight: 600; color: #991B1B;">Not Configured</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("Configure API Key", expanded=False):
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
                    
        st.divider()
        
        # Compact Demo Data & Clear State Section with Confirmations
        st.markdown(
            """
            <div style="font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px;">
                DEMO DATA MANAGEMENT
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
                <div style="font-size: 12px; color: #166534; background: #F0FDF4; border: 1px solid #BBF7D0; padding: 8px 10px; border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-weight: 600;">✓ Demo Dataset Active</div>
                    <div style="font-size: 11px; color: #15803D; margin-top: 2px;">8 realistic sample subscriptions loaded.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if not st.session_state.get("confirm_clear_prompt"):
                if st.button("Clear Demo Data", use_container_width=True):
                    st.session_state["confirm_clear_prompt"] = True
                    st.rerun()
            else:
                st.warning("Are you sure? This will remove all sample subscriptions.")
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    if st.button("Confirm", type="primary", use_container_width=True):
                        st.session_state["subscriptions"] = []
                        st.session_state["audit_result"] = None
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
                <div style="font-size: 11px; color: #64748B; margin-bottom: 8px;">
                    Explore SubSight AI with realistic sample subscriptions.
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
                        st.session_state["subscriptions"] = get_demo_subscriptions()
                        st.toast("Loaded demo subscription dataset!", icon="🚀")
                        st.rerun()
            else:
                st.warning("Loading demo data will replace your current subscriptions. Proceed?")
                l_col1, l_col2 = st.columns(2)
                with l_col1:
                    if st.button("Load", type="primary", use_container_width=True):
                        st.session_state["subscriptions"] = get_demo_subscriptions()
                        st.session_state["confirm_load_prompt"] = False
                        st.toast("Loaded demo subscriptions!", icon="🚀")
                        st.rerun()
                with l_col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state["confirm_load_prompt"] = False
                        st.rerun()
                        
        # Destructive Clear All Data option if user has custom data
        if has_subs and not has_demo:
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if not st.session_state.get("confirm_clear_user_prompt"):
                if st.button("Clear All Data", use_container_width=True):
                    st.session_state["confirm_clear_user_prompt"] = True
                    st.rerun()
            else:
                st.warning("Are you sure? This will remove all current subscriptions from this session.")
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    if st.button("Clear Data", type="primary", use_container_width=True):
                        st.session_state["subscriptions"] = []
                        st.session_state["audit_result"] = None
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
            <div style="font-size: 11px; color: #64748B; padding-top: 16px; border-top: 1px solid #E2E8F0; margin-top: 24px;">
                <div style="font-weight: 700; color: #172554;">SubSight AI</div>
                <div style="color: #64748B; margin-bottom: 8px;">B.Tech Capstone · v1.0</div>
                <a href="{GITHUB_REPO_URL}" target="_blank" style="color: #2563EB; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                    <span>↗</span> View source on GitHub
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    return selected_page
