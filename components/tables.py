"""
Table rendering and data editor components for SubSight AI.
"""

from datetime import date
from typing import List, Dict, Any, Tuple
import pandas as pd
import streamlit as st
from utils.validators import CATEGORIES, BILLING_CYCLES, STATUSES, CURRENCIES, sanitize_subscription
from utils.calculations import enrich_subscription_dataframe

def render_dashboard_subscription_table(df: pd.DataFrame):
    """
    Render clean, compact subscription table for Dashboard.
    """
    if df is None or df.empty:
        st.info("No subscriptions tracked yet. Click 'Load Demo Data' in sidebar or add your first subscription.")
        return
        
    enriched = enrich_subscription_dataframe(df)
    
    # Prepare display dataframe
    display_df = enriched[[
        "service", "category", "price", "billing_cycle", "monthly_cost", "renewal_date", "status"
    ]].copy()
    
    display_df.columns = [
        "Service", "Category", "Price", "Cycle", "Monthly Equiv (₹)", "Renewal Date", "Status"
    ]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Service": st.column_config.TextColumn("Service", width="medium"),
            "Category": st.column_config.TextColumn("Category", width="small"),
            "Price": st.column_config.NumberColumn("Price", format="₹%.2f", width="small"),
            "Cycle": st.column_config.TextColumn("Cycle", width="small"),
            "Monthly Equiv (₹)": st.column_config.NumberColumn("Monthly Equiv", format="₹%.2f", width="small"),
            "Renewal Date": st.column_config.DateColumn("Renewal Date", format="YYYY-MM-DD", width="small"),
            "Status": st.column_config.SelectboxColumn("Status", options=STATUSES, width="small"),
        }
    )

def render_editable_subscriptions_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render st.data_editor allowing live edits to price, status, renewal date, etc.
    Guarantees underlying renewal_date column data type matches ColumnDataKind.DATE for st.column_config.DateColumn.
    Returns the edited DataFrame.
    """
    if df is None or df.empty:
        return pd.DataFrame()
        
    enriched = enrich_subscription_dataframe(df)
    
    # Ensure renewal_date column is datetime.date type for st.data_editor DateColumn
    if "renewal_date" in enriched.columns:
        parsed_dates = pd.to_datetime(enriched["renewal_date"], errors="coerce")
        today_ts = pd.Timestamp(date.today())
        enriched["renewal_date"] = parsed_dates.fillna(today_ts).dt.date
    
    # Keep ID and fields for editing
    edit_df = enriched[[
        "id", "service", "category", "price", "currency", "billing_cycle", "renewal_date", "status"
    ]].copy()
    
    edited = st.data_editor(
        edit_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "id": st.column_config.TextColumn("ID", disabled=True, width="small"),
            "service": st.column_config.TextColumn("Service Name", required=True, width="medium"),
            "category": st.column_config.SelectboxColumn("Category", options=CATEGORIES, required=True, width="small"),
            "price": st.column_config.NumberColumn("Price", min_value=0.0, step=10.0, format="%.2f", required=True, width="small"),
            "currency": st.column_config.SelectboxColumn("Currency", options=list(CURRENCIES.keys()), required=True, width="small"),
            "billing_cycle": st.column_config.SelectboxColumn("Billing Cycle", options=BILLING_CYCLES, required=True, width="small"),
            "renewal_date": st.column_config.DateColumn("Renewal Date", format="YYYY-MM-DD", required=True, width="medium"),
            "status": st.column_config.SelectboxColumn("Status", options=STATUSES, required=True, width="small"),
        },
        key="sub_data_editor"
    )
    
    return edited

def filter_subscriptions(df: pd.DataFrame, search_query: str, selected_category: str, selected_status: str) -> pd.DataFrame:
    """
    Filter DataFrame by search query, category, and status.
    """
    if df is None or df.empty:
        return df
        
    filtered = df.copy()
    
    if search_query and search_query.strip():
        q = search_query.strip().lower()
        filtered = filtered[filtered["service"].str.lower().str.contains(q, na=False)]
        
    if selected_category and selected_category != "All Categories":
        filtered = filtered[filtered["category"] == selected_category]
        
    if selected_status and selected_status != "All Statuses":
        filtered = filtered[filtered["status"] == selected_status]
        
    return filtered
