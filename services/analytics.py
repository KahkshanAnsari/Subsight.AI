"""
Analytics and data aggregation services for SubSight AI.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any
import pandas as pd
from utils.validators import sanitize_subscription
from utils.calculations import enrich_subscription_dataframe

def get_demo_subscriptions() -> List[Dict[str, Any]]:
    """
    Returns realistic sample subscription data with Indian Rupee (INR) pricing.
    Covers diverse categories, billing cycles, and status states.
    """
    today = date.today()
    
    raw_demo = [
        {
            "id": "sub_demo_01",
            "service": "Netflix Premium",
            "category": "Entertainment",
            "price": 649.00,
            "currency": "INR (₹)",
            "billing_cycle": "Monthly",
            "renewal_date": (today + timedelta(days=4)).strftime("%Y-%m-%d"),
            "status": "Review Needed",
            "created_at": (today - timedelta(days=120)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_02",
            "service": "Spotify Individual",
            "category": "Entertainment",
            "price": 119.00,
            "currency": "INR (₹)",
            "billing_cycle": "Monthly",
            "renewal_date": (today + timedelta(days=12)).strftime("%Y-%m-%d"),
            "status": "Active",
            "created_at": (today - timedelta(days=300)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_03",
            "service": "YouTube Premium",
            "category": "Entertainment",
            "price": 129.00,
            "currency": "INR (₹)",
            "billing_cycle": "Monthly",
            "renewal_date": (today + timedelta(days=18)).strftime("%Y-%m-%d"),
            "status": "Active",
            "created_at": (today - timedelta(days=200)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_04",
            "service": "Amazon Prime",
            "category": "Shopping",
            "price": 1499.00,
            "currency": "INR (₹)",
            "billing_cycle": "Yearly",
            "renewal_date": (today + timedelta(days=45)).strftime("%Y-%m-%d"),
            "status": "Active",
            "created_at": (today - timedelta(days=320)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_05",
            "service": "Canva Pro",
            "category": "Productivity",
            "price": 3999.00,
            "currency": "INR (₹)",
            "billing_cycle": "Yearly",
            "renewal_date": (today + timedelta(days=6)).strftime("%Y-%m-%d"),
            "status": "Review Needed",
            "created_at": (today - timedelta(days=350)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_06",
            "service": "Google One 100GB",
            "category": "Cloud & Storage",
            "price": 130.00,
            "currency": "INR (₹)",
            "billing_cycle": "Monthly",
            "renewal_date": (today + timedelta(days=22)).strftime("%Y-%m-%d"),
            "status": "Active",
            "created_at": (today - timedelta(days=180)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_07",
            "service": "Notion Plus",
            "category": "Productivity",
            "price": 800.00,
            "currency": "INR (₹)",
            "billing_cycle": "Monthly",
            "renewal_date": (today + timedelta(days=9)).strftime("%Y-%m-%d"),
            "status": "Active",
            "created_at": (today - timedelta(days=90)).strftime("%Y-%m-%d")
        },
        {
            "id": "sub_demo_08",
            "service": "Adobe Creative Cloud",
            "category": "Productivity",
            "price": 4230.00,
            "currency": "INR (₹)",
            "billing_cycle": "Monthly",
            "renewal_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
            "status": "Review Needed",
            "created_at": (today - timedelta(days=400)).strftime("%Y-%m-%d")
        }
    ]
    
    return [sanitize_subscription(item) for item in raw_demo]

def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate monthly spend and subscription counts by category.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["category", "monthly_cost", "annual_cost", "count", "share_pct"])
    
    enriched = enrich_subscription_dataframe(df)
    active = enriched[enriched["status"].isin(["Active", "Review Needed"])]
    
    if active.empty:
        return pd.DataFrame(columns=["category", "monthly_cost", "annual_cost", "count", "share_pct"])
    
    grouped = active.groupby("category").agg(
        monthly_cost=("monthly_cost", "sum"),
        annual_cost=("annual_cost", "sum"),
        count=("id", "count")
    ).reset_index()
    
    total_monthly = float(grouped["monthly_cost"].sum())
    if total_monthly > 0:
        grouped["share_pct"] = (grouped["monthly_cost"] / total_monthly * 100.0).round(1)
    else:
        grouped["share_pct"] = 0.0
        
    return grouped.sort_values(by="monthly_cost", ascending=False)

def get_upcoming_renewals(df: pd.DataFrame, days_ahead: int = 30) -> List[Dict[str, Any]]:
    """
    Find subscriptions renewing within `days_ahead` days.
    Sorted by closest renewal date. Safe for string or date objects.
    """
    if df is None or df.empty:
        return []
    
    enriched = enrich_subscription_dataframe(df)
    active = enriched[enriched["status"].isin(["Active", "Review Needed"])].copy()
    
    today = date.today()
    renewals = []
    
    for _, row in active.iterrows():
        try:
            r_date = row["renewal_date"]
            if isinstance(r_date, (datetime, date)):
                ren_date = r_date.date() if isinstance(r_date, datetime) else r_date
            else:
                ren_date = datetime.strptime(str(r_date).strip(), "%Y-%m-%d").date()
                
            delta_days = (ren_date - today).days
            
            if 0 <= delta_days <= days_ahead:
                renewals.append({
                    "id": row["id"],
                    "service": row["service"],
                    "category": row["category"],
                    "price": row["price"],
                    "billing_cycle": row["billing_cycle"],
                    "monthly_cost": row["monthly_cost"],
                    "renewal_date": ren_date.strftime("%Y-%m-%d"),
                    "days_remaining": delta_days,
                    "status": row["status"]
                })
        except (ValueError, TypeError):
            continue
            
    # Sort by days_remaining ascending
    renewals.sort(key=lambda x: x["days_remaining"])
    return renewals

def get_top_expensive_services(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Get top N most expensive active subscriptions by monthly equivalent cost.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    enriched = enrich_subscription_dataframe(df)
    active = enriched[enriched["status"].isin(["Active", "Review Needed"])]
    
    return active.sort_values(by="monthly_cost", ascending=False).head(top_n)

def get_billing_cycle_split(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate costs by billing cycle (Monthly, Quarterly, Yearly).
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["billing_cycle", "monthly_cost", "count"])
    
    enriched = enrich_subscription_dataframe(df)
    active = enriched[enriched["status"].isin(["Active", "Review Needed"])]
    
    grouped = active.groupby("billing_cycle").agg(
        monthly_cost=("monthly_cost", "sum"),
        annual_cost=("annual_cost", "sum"),
        count=("id", "count")
    ).reset_index()
    
    return grouped
