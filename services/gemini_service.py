"""
Google Gemini AI Service integration for SubSight AI using the official google-genai SDK.
Handles API key resolution, prompt construction, structured output, and fallback models.
"""

import os
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import streamlit as st
from utils.calculations import enrich_subscription_dataframe, calculate_portfolio_metrics
from services.analytics import get_category_breakdown

SUPPORTED_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]

def get_api_key() -> Optional[str]:
    """
    Retrieve Gemini API key from session state, secrets.toml, or environment.
    """
    try:
        if "custom_api_key" in st.session_state and st.session_state["custom_api_key"]:
            return str(st.session_state["custom_api_key"]).strip()
    except Exception:
        pass
    
    try:
        if "GEMINI_API_KEY" in st.secrets and str(st.secrets["GEMINI_API_KEY"]).strip():
            return str(st.secrets["GEMINI_API_KEY"]).strip()
        if "GEMINI_KEY" in st.secrets and str(st.secrets["GEMINI_KEY"]).strip():
            return str(st.secrets["GEMINI_KEY"]).strip()
    except Exception:
        pass
    
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
        
    return None

def verify_gemini_client() -> Tuple[bool, Optional[Any], str]:
    """
    Verify and instantiate Google GenAI client.
    Returns (is_configured, client_instance, status_message)
    """
    api_key = get_api_key()
    if not api_key:
        return False, None, "Not Configured (Missing API Key)"
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return True, client, "Connected (Gemini Engine)"
    except Exception as e:
        return False, None, f"Configuration Error: {str(e)}"

def build_audit_prompt(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Build structured system instructions and dynamic context payload from real user data.
    """
    enriched = enrich_subscription_dataframe(df)
    metrics = calculate_portfolio_metrics(df)
    cat_df = get_category_breakdown(df)
    
    sub_lines = []
    for idx, row in enriched.iterrows():
        sub_lines.append(
            f"- {row['service']} | Category: {row['category']} | Price: {row['currency']}{row['price']:,.2f} ({row['billing_cycle']}) "
            f"| Monthly Equiv: ₹{row['monthly_cost']:,.2f} | Status: {row['status']} | Renewal: {row['renewal_date']}"
        )
    sub_data_str = "\n".join(sub_lines) if sub_lines else "No active subscriptions."
    
    cat_lines = []
    for idx, row in cat_df.iterrows():
        cat_lines.append(f"- {row['category']}: ₹{row['monthly_cost']:,.2f}/month ({row['share_pct']:.1f}% share)")
    cat_data_str = "\n".join(cat_lines) if cat_lines else "None"
    
    system_prompt = """
You are SubSight AI — a strict, practical personal subscription financial analyst.

Your primary objective is to help the user eliminate waste, uncover redundant service overlaps, and maximize annual savings.

CRITICAL OPERATIONAL CONSTRAINTS:
1. Reason STRICTLY from the user's provided subscription data below. NEVER invent or hallucinate services, prices, renewal dates, or usage statistics not explicitly present.
2. Identify potential service overlaps (e.g. streaming duplicates like Netflix, Spotify, Amazon Prime, YouTube Premium; productivity overlap like Canva, Notion, Adobe CC).
3. Do NOT blindly tell the user to cancel everything. Provide balanced trade-offs distinguishing core productivity tools from optional entertainment.
4. Format your output clearly using Markdown headers, bulleted lists, structured callouts, and clean tables.
""".strip()

    user_context = f"""
USER PORTFOLIO DATA FOR SUBSCRIPTION AUDIT:

=== ACTIVE SUBSCRIPTION DATASET ===
{sub_data_str}

=== FINANCIAL PORTFOLIO OVERVIEW ===
- Total Tracked Subscriptions: {metrics['total_count']}
- Total Active & Review Needed Subscriptions: {metrics['active_count']}
- Total Monthly Spend Commitment: ₹{metrics['total_monthly']:,.2f}
- Total Annual Projected Spend: ₹{metrics['total_annual']:,.2f}
- Flagged Review Needed Count: {metrics['review_needed_count']}

=== CATEGORY EXPENDITURE BREAKDOWN ===
{cat_data_str}

REQUIRED AUDIT OUTPUT SECTIONS:
### 1. OVERALL ASSESSMENT
(Provide a 2-3 sentence executive summary of portfolio health and spending rate.)

### 2. SPENDING BREAKDOWN & SERVICE OVERLAP ANALYSIS
(Analyze category concentration and point out specific overlapping service pairs or redundant tier plans.)

### 3. TOP SAVINGS OPPORTUNITIES
(Detail specific subscriptions recommended for review or cancellation with monthly & annual savings.)

### 4. POTENTIAL ANNUAL SAVINGS SUMMARY
(State exact total monthly savings and annual savings projection in Rupees.)

### 5. RECOMMENDATION CLASSIFICATION TABLE
(Provide a markdown table with columns: Service | Monthly Cost | Category | Recommendation [KEEP / REVIEW / CANCEL] | Rationale)

### 6. ACTION PLAN
(3-4 numbered execution steps for the user.)
""".strip()

    return system_prompt, user_context

def run_ai_audit(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Execute full portfolio AI Audit using google-genai SDK with model fallback logic.
    """
    if df.empty:
        return False, "No subscriptions available to audit. Please add subscriptions or load demo data."
    
    is_configured, client, status_msg = verify_gemini_client()
    if not is_configured or client is None:
        return False, f"Gemini API is not configured: {status_msg}. Please enter a valid API key in the sidebar."
    
    system_prompt, user_context = build_audit_prompt(df)
    
    from google.genai import types
    
    last_err = ""
    for model_name in SUPPORTED_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_context,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                    max_output_tokens=2048,
                )
            )
            if response and response.text and response.text.strip():
                return True, response.text.strip()
        except Exception as e:
            last_err = str(e)
            continue
            
    # Clean user-friendly error message
    if "API_KEY_INVALID" in last_err or "400" in last_err or "403" in last_err:
        return False, "The provided Gemini API key is invalid or unauthorized. Please check your API key."
    elif "RESOURCE_EXHAUSTED" in last_err or "429" in last_err:
        return False, "Gemini API rate limit or quota exceeded. Please wait a moment and try again."
    else:
        return False, f"Unable to reach Gemini API. Details: {last_err}"

def run_savings_scenario_analysis(df: pd.DataFrame, cancel_ids: list, sim_metrics: dict) -> Tuple[bool, str]:
    """
    Generate targeted AI trade-off evaluation for a selected cancellation scenario.
    """
    if not cancel_ids:
        return False, "No subscriptions selected for cancellation simulation."
        
    is_configured, client, status_msg = verify_gemini_client()
    if not is_configured or client is None:
        return False, "Gemini API key is required to evaluate scenario trade-offs."
        
    enriched = enrich_subscription_dataframe(df)
    cancelled_subs = enriched[enriched["id"].isin(cancel_ids)]
    kept_subs = enriched[~enriched["id"].isin(cancel_ids) & enriched["status"].isin(["Active", "Review Needed"])]
    
    cancel_str = "\n".join([f"- {r['service']} (₹{r['monthly_cost']:,.2f}/mo, Category: {r['category']})" for _, r in cancelled_subs.iterrows()])
    kept_str = "\n".join([f"- {r['service']} (₹{r['monthly_cost']:,.2f}/mo, Category: {r['category']})" for _, r in kept_subs.iterrows()]) if not kept_subs.empty else "None (All subscriptions cancelled)"
    
    prompt = f"""
You are SubSight AI. The user is simulating a subscription cancellation scenario.

=== CANCELLATION SCENARIO DATA ===
Subscriptions Selected for Cancellation:
{cancel_str}

Subscriptions Remaining Active:
{kept_str}

Financial Impact:
- Current Monthly Spend: ₹{sim_metrics['current_monthly']:,.2f}
- New Monthly Spend: ₹{sim_metrics['new_monthly']:,.2f}
- Monthly Savings: ₹{sim_metrics['monthly_savings']:,.2f}
- Projected Annual Savings: ₹{sim_metrics['annual_savings']:,.2f} ({sim_metrics['savings_percentage']:.1f}% reduction)

TASK:
Provide a concise, sharp evaluation of this specific cancellation scenario:
1. **Financial Impact Assessment**: Evaluate if this is a high-yield cut.
2. **Functional & Content Trade-offs**: Detail specific features or content lost (e.g. YouTube Music included with YT Premium, Canva templates, cloud storage tier changes).
3. **Execution Advice**: 1-2 actionable tips for executing these cancellations cleanly.
Keep response structured under clear Markdown headings.
"""
    from google.genai import types
    
    last_err = ""
    for model_name in SUPPORTED_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=1024,
                )
            )
            if response and response.text and response.text.strip():
                return True, response.text.strip()
        except Exception as e:
            last_err = str(e)
            continue
            
    return False, f"AI Analysis Error: {last_err}"
