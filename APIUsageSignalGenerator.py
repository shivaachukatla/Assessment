import json
import os
from collections import defaultdict
from simple_salesforce import Salesforce
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# --- Load environment variables ---
load_dotenv()
USERNAME = os.getenv("SF_USERNAME")
PASSWORD = os.getenv("SF_PASSWORD")
SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")

# --- Initialize LLM and Salesforce ---
llm = ChatOpenAI()
sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)

# --- Fetch config from Salesforce ---
def fetch_config(signal_type="Product Usage Trend"):
    config_query = f"""
    SELECT Id, Data_Source__c, Prompt_Template__c, Query__c, Signal_Type__c
    FROM Customer_Signal_Generation_Config__c
    WHERE Signal_Type__c = 'Product Usage Trends'
    LIMIT 1
    """
    result = sf.query(config_query)
    if not result['records']:
        raise Exception(f"No config found for signal type: {signal_type}")
    return result['records'][0]

# --- Load config and prompt ---
config = fetch_config()
prompt_template = config['Prompt_Template__c']

# --- Load usage data from local file (demo use) ---
with open("api_usage_data.json", "r") as f:
    usage_data = json.load(f)

# --- Group usage data by customer_id ---
usage_by_customer = defaultdict(list)
for record in usage_data:
    customer_id = record.get("customer_id")
    month = record.get("month")
    api_calls = record.get("api_calls")

    if customer_id and month and api_calls is not None:
        usage_by_customer[customer_id].append(f"Month: {month}, API Calls: {api_calls}")

# --- Input: choose customer or all ---
input_customer_id = input("Enter Customer ID (or leave blank for all): ").strip()
run_for_all = input_customer_id == ""

# --- Generate signal(s) ---
for customer_id, usage_lines in usage_by_customer.items():
    if not run_for_all and customer_id != input_customer_id:
        continue  # Skip if not the specified customer
    
    combined_text = "\n".join(usage_lines)
    prompt = prompt_template.replace("{combined_text}", combined_text).replace("{customer_id}", customer_id)
    
    response = llm.invoke(prompt)
    
    print(f"\nCustomer ID: {customer_id}")
    print("Product Usage Trend Analysis:")
    print(response.content)
    print("-" * 50)
