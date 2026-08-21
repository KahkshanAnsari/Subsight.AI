"""
Reusable card and metric components for SubSight AI.
"""

from typing import Dict, Any, List
import streamlit as st

def render_kpi_cards(metrics: Dict[str, Any], has_demo_data: bool = False):
    """
    Render top 4 SaaS KPI metric cards using st.metric with clean layout.
    """
    col1, col2, col3, col4 = st.columns(4)
    
    status_label = "Demo Dataset" if has_demo_data else "User Dataset"
    
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
            label="Annual Spend",
            value=f"₹{metrics['total_annual']:,.2f}",
            delta="12-Month Projection",
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

def render_ai_snapshot_card(audit_result: Any, on_run_audit_cb):
    """
    Render the compact AI Snapshot card on the Dashboard.
    """
    st.markdown(
        """
        <div class="saas-card" style="margin-top: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div style="font-size: 15px; font-weight: 700; color: #172554; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px;">🤖</span> AI Intelligence Snapshot
                </div>
                <span style="font-size: 10px; font-weight: 700; color: #2563EB; background: #EFF6FF; border: 1px solid #BFDBFE; padding: 4px 8px; border-radius: 12px; letter-spacing: 0.5px;">
                    GEMINI 2.5 ENGINE
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
            <div style="font-size: 13px; color: #334155; line-height: 1.6; margin-bottom: 16px; background: #F8FAFC; padding: 12px 14px; border-left: 3px solid #2563EB; border-radius: 0 4px 4px 0;">
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
                Run your first AI Audit to uncover potential savings, detect overlapping services, and optimize your recurring subscriptions.
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Run AI Audit Now", type="primary", key="dash_run_audit_btn", use_container_width=True):
            st.session_state["selected_page"] = "AI Audit"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

def render_upcoming_renewal_cards(renewals: List[Dict[str, Any]]):
    """
    Render list of upcoming renewal cards.
    """
    if not renewals:
        st.info("No upcoming renewals within the next 30 days.")
        return
        
    for ren in renewals:
        days = ren["days_remaining"]
        if days <= 3:
            badge_color = "#DC2626"
            badge_bg = "#FEF2F2"
            border_color = "#FECACA"
            urgency = "CRITICAL"
        elif days <= 7:
            badge_color = "#D97706"
            badge_bg = "#FFFBEB"
            border_color = "#FDE68A"
            urgency = "UPCOMING"
        else:
            badge_color = "#2563EB"
            badge_bg = "#EFF6FF"
            border_color = "#BFDBFE"
            urgency = "SCHEDULED"
            
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid {border_color}; border-left: 4px solid {badge_color}; padding: 14px 16px; border-radius: 8px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div>
                    <div style="font-weight: 700; color: #111827; font-size: 14px; margin-bottom: 2px;">{ren['service']}</div>
                    <div style="font-size: 12px; color: #64748B;">
                        {ren['category']} • Renews {ren['renewal_date']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 800; color: #172554; font-size: 14px;">₹{ren['price']:,.2f} <span style="font-size: 11px; font-weight: 500; color: #64748B;">/{ren['billing_cycle'][:2].lower()}</span></div>
                    <div style="font-size: 10px; font-weight: 700; color: {badge_color}; background: {badge_bg}; padding: 2px 6px; border-radius: 4px; margin-top: 4px; display: inline-block;">
                        {days} Days Left ({urgency})
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
