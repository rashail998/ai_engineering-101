import pandas as pd
import anthropic
import json
from dotenv import load_dotenv
load_dotenv()

# Load the cleaned dataset here
df = pd.read_csv('sales_data_cleaned.csv')

# 1. Use pandas to build a compact summary

summary = {
    "total_orders" : len(df),
    "date_range" : f"{df['date'].min()} to {df['date'].max()}",
    "total_revenue_EUR" : round(df['order_value_EUR'].sum(), 2),
    "total_cost_EUR" : round(df['cost'].sum(), 2),
    "revenue_by_category" : df.groupby('category')['order_value_EUR'].sum().round(2).to_dict(),
    "revenue_by_country" : df.groupby('country')['order_value_EUR'].sum().round(2).to_dict(),
    "orders_by_device_type" : df['device_type'].value_counts().to_dict(),
    "top_5_sales_reps_by_revenue" : df.groupby('sales_rep')['order_value_EUR'].sum().sort_values(ascending=False).head(5).round(2).to_dict()
}


# 2. Build the prompt to send to Claude
prompt = f"""You are a sales data analyst. Here is a summary of a sales dataset:

{json.dumps(summary, indent=2, default=str)}

Analyze this data and respond ONLY with a valid JSON (no markdown, no explanation outside the JSON) in this exact format:

{{
    "headline_insight": "one sentence, the single most important finding",
    "top_performing_category": "category name",
    "top_performing_country": "country name",
    "profit_margin_percent": <number, calculated as (revenue-cost)/revenue * 100>,
    "concerns": ["list of any red flags or risks you notice"],
    "recommendations": ["2-3 actionable business recommendations"]
}}

"""


# 3. Call Claude

client = anthropic.Anthropic()

response = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 500,
    messages = [{"role": "user", "content": prompt}]
)

raw_output = response.content[0].text


# 4. Parse JSON response

try:
    insights = json.loads(raw_output)
    print("\nSuccessfully parsed structured insights:\n")
    print(json.dumps(insights, indent=2))

except json.JSONDecodeError:
    print("\nClaude didn't return valid JSON. Raw output was:\n")
    print(raw_output)