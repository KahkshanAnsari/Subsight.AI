"""
Reusable card and metric components for SubSight AI.
Premium SaaS / Fintech Design System.
"""

from typing import Dict, Any, List
import streamlit as st

def render_kpi_cards(metrics: Dict[str, Any], has_demo_data: bool = False):
    """
    Render top 4 SaaS KPI metric cards using st.metric with clean layout.
    """
    col1, col2, col3, col4 = st.columns(4)
    
    status_label = "Demo Dataset" if has_demo_data else "Live Portfolio"
    
    with col1:
        st.metric(
            label="Monthly Spend",
            value=f"₹{metrics['total_monthly']:,.2f}",
            delta=f"{status_label}",
            delta_color="off",
            help="Total monthly commitment across all active subscriptions"
        )
        
    with col2:
        st.metric(
            label="Annual Projection",
            value=f"₹{metrics['total_annual']:,.2f}",
            delta="12-Month Run Rate",
            delta_color="off",
            help="Projected yearly recurring expense based on active plans"
        )
        
    with col3:
        st.metric(
            label="Active Subscriptions",
            value=f"{metrics['active_count']}",
            delta=f"{metrics['total_count']} Total Tracked",
            delta_color="normal",
            help="Count of currently active and review-needed subscriptions"
        )
        
    with col4:
        st.metric(
            label="Potential Savings",
            value=f"₹{metrics['potential_annual_savings']:,.2f}/yr",
            delta=f"{metrics['review_needed_count']} Flagged for Review" if metrics['review_needed_count'] > 0 else "0 Flagged",
            delta_color="normal",
            help="Estimated annual savings from subscriptions flagged for review or cancellation"
        )

def render_ai_snapshot_card(audit_result: Any, on_run_audit_cb=None):
    """
    Render the compact AI Snapshot card on the Dashboard.
    """
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:20px 22px; margin-top:10px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
                <div style="font-size: 13px; font-weight: 700; color: #0F172A; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 16px;">🤖</span> AI Intelligence Snapshot
                </div>
                <span style="font-size: 9px; font-weight: 700; color: #7C3AED; background: #F5F3FF; border: 1px solid #DDD6FE; padding: 3px 8px; border-radius: 10px; letter-spacing: 0.5px;">
                    GEMINI 2.5
                </span>
            </div>
        """,
        unsafe_allow_html=True
    )
    
    if audit_result and isinstance(audit_result, str):
        # Snippet of audit result
        snippet = audit_result[:250] + "..." if len(audit_result) > 250 else audit_result
        st.markdown(
            f"""
            <div style="font-size: 13px; color: #334155; line-height: 1.6; margin-bottom: 16px; background: #F8FAFC; padding: 12px 14px; border-left: 3px solid #7C3AED; border-radius: 0 6px 6px 0;">
                {snippet}
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("View Full AI Audit & Recommendations →", key="view_audit_btn", use_container_width=True):
            st.session_state["selected_page"] = "AI Audit"
            st.rerun()
    else:
        st.markdown(
            """
            <div style="font-size: 13px; color: #64748B; line-height: 1.5; margin-bottom: 16px;">
                Run your portfolio audit to uncover potential savings, detect overlapping services, and optimize recurring expenses.
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Generate AI Audit Now", type="primary", key="dash_run_audit_btn", use_container_width=True):
            st.session_state["selected_page"] = "AI Audit"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

def render_upcoming_renewal_cards(renewals: List[Dict[str, Any]]):
    """
    Render list of upcoming renewal cards with polished fintech badges.
    """
    if not renewals:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px dashed #E2E8F0; border-radius: 10px; padding: 24px; text-align: center; color: #94A3B8; font-size: 13px;">
                No renewals due in the next 30 days.
            </div>
            """,
            unsafe_allow_html=True
        )
        return
        
    for ren in renewals:
        days = ren["days_remaining"]
        if days <= 3:
            badge_color = "#DC2626"
            badge_bg = "#FEF2F2"
            border_color = "#FECACA"
            accent_bar = "#DC2626"
            urgency = "URGENT"
        elif days <= 7:
            badge_color = "#D97706"
            badge_bg = "#FFFBEB"
            border_color = "#FDE68A"
            accent_bar = "#D97706"
            urgency = "SOON"
        else:
            badge_color = "#2563EB"
            badge_bg = "#EFF6FF"
            border_color = "#BFDBFE"
            accent_bar = "#2563EB"
            urgency = "SCHEDULED"
            
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 3px solid {accent_bar}; padding: 12px 14px; border-radius: 8px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div>
                    <div style="font-weight: 600; color: #0F172A; font-size: 13px; margin-bottom: 2px;">{ren['service']}</div>
                    <div style="font-size: 11px; color: #64748B;">
                        {ren['category']} · {ren['renewal_date']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #0F172A; font-size: 13px;">₹{ren['price']:,.2f} <span style="font-size: 10px; font-weight: 500; color: #64748B;">/{ren['billing_cycle'][:2].lower()}</span></div>
                    <div style="font-size: 9px; font-weight: 700; color: {badge_color}; background: {badge_bg}; padding: 2px 7px; border-radius: 10px; margin-top: 3px; display: inline-block; letter-spacing: 0.3px;">
                        {days}d · {urgency}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
