from simple_salesforce import Salesforce
from datetime import datetime
import pytz
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from collections import defaultdict
import os

# --- Load credentials from .env file ---
load_dotenv()

USERNAME = os.getenv("SF_USERNAME")
PASSWORD = os.getenv("SF_PASSWORD")
SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")

llm = ChatOpenAI()

# --- Connect to Salesforce ---
sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)

# --- Step 1: Fetch config from custom object ---
def fetch_config(signal_type="Case Sentiment"):
    config_query = f"""
    SELECT Id, Data_Source__c, Prompt_Template__c, Query__c, Signal_Type__c
    FROM Customer_Signal_Generation_Config__c
    WHERE Signal_Type__c = '{signal_type}'
    LIMIT 1
    """
    result = sf.query(config_query)
    if not result['records']:
        raise Exception(f"No config found for signal type: {signal_type}")
    return result['records'][0]

config = fetch_config()
data_query = config['Query__c']
prompt_template = config['Prompt_Template__c']

# --- Step 2: Execute query to get case data ---
results = sf.query(data_query)
print(f"Total records found: {results['totalSize']}")

# --- Step 3: Group by AccountId ---
cases_by_account = defaultdict(list)
for record in results['records']:
    if record.get('Description'):
        cases_by_account[record['AccountId']].append(record['Description'])

# --- Step 4: Generate signal per account ---
for account_id, descriptions in cases_by_account.items():
    combined_text = "\n".join(descriptions)
    prompt = prompt_template.replace("{combined_text}", combined_text)

    response = llm.invoke(prompt)
    
    print(f"\nAccount ID: {account_id}")
    print("Sentiment Analysis:")
    print(response.content)
    print("-" * 50)