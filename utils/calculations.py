"""
Financial math and calculation helpers for SubSight AI.
Note: Unrounded floating point calculations are maintained internally to avoid
truncation drift across calculations. Rounding is applied only during display formatting.
"""

from datetime import date
from typing import Dict, List, Any
import pandas as pd

def calculate_monthly_equivalent(price: float, billing_cycle: str) -> float:
    """
    Convert any billing cycle price to standard monthly cost equivalent without internal rounding.
    - Monthly: price
    - Quarterly: price / 3.0
    - Yearly: price / 12.0
    """
    price = max(0.0, float(price))
    cycle = str(billing_cycle).strip().lower()
    
    if cycle == "yearly":
        return price / 12.0
    elif cycle == "quarterly":
        return price / 3.0
    else:
        # Default to monthly
        return price

def calculate_annual_equivalent(monthly_cost: float) -> float:
    """Calculate exact annual projection from monthly cost without internal rounding."""
    return max(0.0, float(monthly_cost)) * 12.0

def calculate_percentage_change(current: float, previous: float) -> float:
    """
    Safely calculate percentage change.
    Returns 0.0 if previous is 0 to avoid zero division.
    """
    if previous <= 0:
        return 0.0
    return ((current - previous) / previous) * 100.0

def enrich_subscription_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich raw subscriptions DataFrame with exact computed fields & proper data types:
    - monthly_cost (float)
    - annual_cost (float)
    - renewal_date (datetime.date)
    """
    cols = [
        "id", "service", "category", "price", "currency", 
        "billing_cycle", "monthly_cost", "annual_cost", 
        "renewal_date", "status", "created_at"
    ]

    if df is None or df.empty:
        empty_df = pd.DataFrame(columns=cols)
        empty_df["renewal_date"] = pd.to_datetime(empty_df["renewal_date"]).dt.date
        return empty_df
    
    enriched = df.copy()
    
    # Ensure numeric price
    enriched["price"] = pd.to_numeric(enriched["price"], errors="coerce").fillna(0.0).astype(float)
    
    # Exact float calculations internally
    enriched["monthly_cost"] = enriched.apply(
        lambda r: calculate_monthly_equivalent(r["price"], r["billing_cycle"]), axis=1
    ).astype(float)
    enriched["annual_cost"] = enriched["monthly_cost"].apply(calculate_annual_equivalent).astype(float)
    
    # Convert renewal_date robustly to datetime.date objects for st.data_editor & Plotly compatibility
    if "renewal_date" in enriched.columns:
        parsed_dates = pd.to_datetime(enriched["renewal_date"], errors="coerce")
        default_today = pd.Timestamp(date.today())
        enriched["renewal_date"] = parsed_dates.fillna(default_today).dt.date
    else:
        enriched["renewal_date"] = date.today()
        
    return enriched

def calculate_portfolio_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate high-level financial metrics from enriched DataFrame with full precision.
    """
    if df is None or df.empty:
        return {
            "total_monthly": 0.0,
            "total_annual": 0.0,
            "active_count": 0,
            "total_count": 0,
            "potential_monthly_savings": 0.0,
            "potential_annual_savings": 0.0,
            "review_needed_count": 0
        }
    
    enriched = enrich_subscription_dataframe(df)
    
    # Active & Review Needed are active commitments
    active_df = enriched[enriched["status"].isin(["Active", "Review Needed"])]
    review_df = enriched[enriched["status"] == "Review Needed"]
    
    total_monthly = float(active_df["monthly_cost"].sum())
    total_annual = float(active_df["annual_cost"].sum())
    active_count = int(len(active_df))
    total_count = int(len(enriched))
    
    # Potential savings = items tagged "Review Needed"
    review_monthly = float(review_df["monthly_cost"].sum())
    review_annual = float(review_df["annual_cost"].sum())
    
    return {
        "total_monthly": total_monthly,
        "total_annual": total_annual,
        "active_count": active_count,
        "total_count": total_count,
        "potential_monthly_savings": review_monthly,
        "potential_annual_savings": review_annual,
        "review_needed_count": int(len(review_df))
    }

def simulate_cancellation_scenario(df: pd.DataFrame, cancel_ids: List[str]) -> Dict[str, Any]:
    """
    Simulate impact of canceling selected subscription IDs with full precision math.
    """
    if df is None or df.empty:
        return {
            "current_monthly": 0.0,
            "new_monthly": 0.0,
            "monthly_savings": 0.0,
            "annual_savings": 0.0,
            "savings_percentage": 0.0,
            "cancelled_count": 0
        }
    
    enriched = enrich_subscription_dataframe(df)
    active_df = enriched[enriched["status"].isin(["Active", "Review Needed"])]
    
    current_monthly = float(active_df["monthly_cost"].sum())
    
    # Remaining active items
    kept_df = active_df[~active_df["id"].isin(cancel_ids)]
    new_monthly = float(kept_df["monthly_cost"].sum())
    
    monthly_savings = max(0.0, current_monthly - new_monthly)
    annual_savings = monthly_savings * 12.0
    
    savings_pct = 0.0
    if current_monthly > 0:
        savings_pct = (monthly_savings / current_monthly) * 100.0
        
    return {
        "current_monthly": current_monthly,
        "new_monthly": new_monthly,
        "monthly_savings": monthly_savings,
        "annual_savings": annual_savings,
        "savings_percentage": savings_pct,
        "cancelled_count": len(cancel_ids)
    }
