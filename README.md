# Summary of SalesforceCaseSentimentGenerator.py

This script connects to Salesforce, fetches case data grouped by Account, and uses an LLM (OpenAI via LangChain) to generate sentiment analysis for each account's case descriptions. Configuration (such as prompts and queries) is dynamically loaded from a Salesforce custom object. Results are printed for each account.

**Main Steps:**
1. Load Salesforce credentials from environment.
2. Fetch signal generation config and relevant case data from Salesforce.
3. Group case descriptions by AccountId.
4. Use an LLM to analyze combined descriptions per account and output the sentiment.

