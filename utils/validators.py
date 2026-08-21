"""
Validation and data sanitization utilities for SubSight AI.
"""

import uuid
from datetime import datetime, date
from typing import Dict, Any, Tuple, Optional

CATEGORIES = [
    "Entertainment",
    "Productivity",
    "Education",
    "Cloud & Storage",
    "Health & Fitness",
    "Shopping",
    "Other"
]

BILLING_CYCLES = ["Monthly", "Quarterly", "Yearly"]

STATUSES = ["Active", "Review Needed", "Paused", "Cancelled"]

CURRENCIES = {
    "INR (₹)": "₹",
    "USD ($)": "$",
    "EUR (€)": "€",
    "GBP (£)": "£"
}

def generate_sub_id() -> str:
    """Generate a clean, unique subscription identifier."""
    return f"sub_{uuid.uuid4().hex[:8]}"

def validate_price(price_input: Any) -> Tuple[bool, float, str]:
    """
    Validate numeric price.
    Returns (is_valid, float_price, error_message)
    """
    try:
        val = float(price_input)
        if val < 0:
            return False, 0.0, "Price cannot be negative."
        if val == 0:
            return False, 0.0, "Price should be greater than 0."
        return True, val, ""
    except (ValueError, TypeError):
        return False, 0.0, "Please enter a valid numeric price."

def validate_date_string(date_input: Any) -> str:
    """Ensure renewal date is a valid YYYY-MM-DD string."""
    if date_input is None:
        return date.today().strftime("%Y-%m-%d")
        
    if isinstance(date_input, (datetime, date)):
        return date_input.strftime("%Y-%m-%d")
        
    if hasattr(date_input, "strftime"):
        try:
            return date_input.strftime("%Y-%m-%d")
        except Exception:
            pass
    
    if isinstance(date_input, str):
        s_date = date_input.strip()
        try:
            parsed = datetime.strptime(s_date, "%Y-%m-%d")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            try:
                parsed = datetime.fromisoformat(s_date)
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                pass

    return date.today().strftime("%Y-%m-%d")

def sanitize_subscription(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize and ensure all required schema fields exist on a subscription dict.
    """
    sub_id = str(raw_data.get("id") or generate_sub_id())
    service = str(raw_data.get("service", "Unnamed Service")).strip()
    category = str(raw_data.get("category", "Other")).strip()
    if category not in CATEGORIES:
        category = "Other"
        
    billing_cycle = str(raw_data.get("billing_cycle", "Monthly")).strip()
    if billing_cycle not in BILLING_CYCLES:
        billing_cycle = "Monthly"
        
    status = str(raw_data.get("status", "Active")).strip()
    if status not in STATUSES:
        status = "Active"
        
    currency = str(raw_data.get("currency", "INR (₹)")).strip()
    if currency not in CURRENCIES:
        currency = "INR (₹)"
        
    _, price, _ = validate_price(raw_data.get("price", 0.0))
    renewal_date = validate_date_string(raw_data.get("renewal_date"))
    created_at = validate_date_string(raw_data.get("created_at"))

    return {
        "id": sub_id,
        "service": service,
        "category": category,
        "price": price,
        "currency": currency,
        "billing_cycle": billing_cycle,
        "renewal_date": renewal_date,
        "status": status,
        "created_at": created_at
    }
