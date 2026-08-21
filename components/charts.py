"""
Interactive Plotly charts for SubSight AI styled matching the SaaS design palette.
"""

from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from services.analytics import get_category_breakdown, get_billing_cycle_split, get_top_expensive_services
from utils.calculations import enrich_subscription_dataframe

COLOR_PALETTE = ["#2563EB", "#172554", "#16A34A", "#D97706", "#9333EA", "#0891B2", "#DC2626", "#64748B"]

def apply_plotly_theme(fig):
    """Apply consistent light-theme layout to Plotly figures."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif", color="#111827", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#64748B")
        ),
        hoverlabel=dict(
            bgcolor="#172554",
            font_size=12,
            font_family="-apple-system, sans-serif"
        )
    )
    return fig

def render_spending_overview_chart(df: pd.DataFrame, view_type: str = "Monthly"):
    """
    Render spending distribution bar chart across services.
    """
    if df is None or df.empty:
        st.info("No subscription data available for chart.")
        return
        
    enriched = enrich_subscription_dataframe(df)
    active = enriched[enriched["status"].isin(["Active", "Review Needed"])].copy()
    
    if active.empty:
        st.info("No active subscriptions to display.")
        return
        
    cost_col = "monthly_cost" if view_type == "Monthly" else "annual_cost"
    label_suffix = "/month" if view_type == "Monthly" else "/year"
    
    active = active.sort_values(by=cost_col, ascending=True)
    
    fig = px.bar(
        active,
        x=cost_col,
        y="service",
        color="category",
        orientation="h",
        labels={cost_col: f"Cost (₹{label_suffix})", "service": "Service", "category": "Category"},
        title=f"Recurring Spending Breakdown ({view_type} Equivalent)",
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Category: %{customdata[0]}<br>Cost: ₹%{x:,.2f}" + label_suffix,
        customdata=active[["category"]]
    )
    
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0", tickprefix="₹")
    fig.update_yaxes(showgrid=False)
    
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_category_donut_chart(df: pd.DataFrame):
    """
    Render category breakdown donut chart.
    """
    if df is None or df.empty:
        st.info("No category data available.")
        return
        
    cat_df = get_category_breakdown(df)
    
    if cat_df is None or cat_df.empty:
        st.info("No category data available.")
        return
        
    fig = px.pie(
        cat_df,
        values="monthly_cost",
        names="category",
        hole=0.55,
        title="Category Spend Share",
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Monthly Spend: ₹%{value:,.2f}<br>Share: %{percent}"
    )
    
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_simulator_comparison_chart(sim_metrics: dict):
    """
    Render Before / After scenario bar chart for Savings Simulator.
    """
    if not sim_metrics:
        st.info("No simulation metrics available.")
        return
        
    scenarios = ["Current Spend", "After Changes"]
    monthly_vals = [sim_metrics.get("current_monthly", 0.0), sim_metrics.get("new_monthly", 0.0)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scenarios,
        y=monthly_vals,
        name="Monthly Spend (₹)",
        marker_color=["#172554", "#16A34A"],
        text=[f"₹{v:,.2f}" for v in monthly_vals],
        textposition="auto"
    ))
    
    fig.update_layout(
        title="Monthly Spend Comparison",
        yaxis=dict(title="Spend (₹)", tickprefix="₹", gridcolor="#E2E8F0"),
        barmode="group"
    )
    
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_top_expensive_chart(df: pd.DataFrame):
    """
    Render top 5 expensive subscriptions bar chart.
    """
    if df is None or df.empty:
        st.info("No data available.")
        return
        
    top_df = get_top_expensive_services(df, top_n=5)
    
    if top_df is None or top_df.empty:
        st.info("No data available.")
        return
        
    fig = px.bar(
        top_df,
        x="service",
        y="monthly_cost",
        color="service",
        text="monthly_cost",
        title="Top 5 Most Expensive Subscriptions (Monthly Equiv)",
        labels={"monthly_cost": "Monthly Cost (₹)", "service": "Service"},
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        texttemplate="₹%{text:,.2f}",
        textposition="outside"
    )
    
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0", tickprefix="₹")
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_billing_cycle_chart(df: pd.DataFrame):
    """
    Render cost split by billing cycle.
    """
    if df is None or df.empty:
        st.info("No billing cycle data available.")
        return
        
    cycle_df = get_billing_cycle_split(df)
    if cycle_df is None or cycle_df.empty:
        return
        
    fig = px.pie(
        cycle_df,
        values="monthly_cost",
        names="billing_cycle",
        title="Cost Distribution by Billing Cycle",
        color_discrete_sequence=["#2563EB", "#D97706", "#16A34A"]
    )
    
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_renewal_timeline_chart(df: pd.DataFrame):
    """
    Render visual renewal timeline roadmap using Plotly.
    Uses actual subscription dataset renewal dates. Safe against empty data.
    """
    if df is None or df.empty:
        st.info("No upcoming renewal timeline data available.")
        return
        
    enriched = enrich_subscription_dataframe(df)
    active = enriched[enriched["status"].isin(["Active", "Review Needed"])].copy()
    
    if active.empty:
        st.info("No active subscriptions for timeline.")
        return
        
    active["renewal_dt"] = pd.to_datetime(active["renewal_date"], errors="coerce")
    active = active.dropna(subset=["renewal_dt"]).sort_values(by="renewal_dt")
    
    if active.empty:
        st.info("No valid renewal dates found.")
        return
        
    max_cost = float(active["monthly_cost"].max()) if not active["monthly_cost"].empty else 1.0
    sizeref = (2.0 * max_cost / (35.0 ** 2)) if max_cost > 0 else 1.0
    
    fig = px.scatter(
        active,
        x="renewal_dt",
        y="service",
        size="monthly_cost",
        color="category",
        labels={"renewal_dt": "Next Renewal Date", "service": "Service", "monthly_cost": "Monthly Cost"},
        title="Subscription Renewal Timeline & Roadmap",
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        marker=dict(sizemode="area", sizeref=sizeref, sizemin=8),
        hovertemplate="<b>%{y}</b><br>Renewal Date: %{x|%Y-%m-%d}<br>Category: %{customdata[0]}<br>Monthly Cost: ₹%{customdata[1]:,.2f}",
        customdata=active[["category", "monthly_cost"]]
    )
    
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0")
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
