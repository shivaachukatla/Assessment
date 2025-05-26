# Summary of SalesforceCaseSentimentGenerator.py

This script connects to Salesforce, fetches case data grouped by Account, and uses an LLM (OpenAI via LangChain) to generate sentiment analysis for each account's case descriptions. Configuration (such as prompts and queries) is dynamically loaded from a Salesforce custom object. Results are printed for each account.

**Main Steps:**
1. Load Salesforce credentials from environment.
2. Fetch signal generation config and relevant case data from Salesforce.
3. Group case descriptions by AccountId.
4. Use an LLM to analyze combined descriptions per account and output the sentiment.

# Summary of APIUsageSignalGenerator.py

This script analyzes API usage trends for customers using data from a local JSON file and generates a product usage trend analysis for each customer via an LLM (OpenAI through LangChain). It loads configuration (including prompt templates) dynamically from Salesforce, and supports generating analysis for a specific customer or all customers.

**Main Steps:**
1. Load Salesforce credentials from environment variables.
2. Connect to Salesforce and fetch the signal generation configuration, including the prompt template.
3. Load API usage data from a local file (`api_usage_data.json`).
4. Group API usage data by customer.
5. Prompt the user to specify a customer ID (or analyze all customers).
6. For each selected customer:
   - Combine the customer's monthly API usage data into a summary string.
   - Fill the prompt template with this usage data and the customer ID.
   - Use an LLM to analyze the usage trend.
   - Print out the generated analysis.

---

**Notes about `api_usage_data.json`:**
- This file contains a list of monthly API usage records for multiple customers.
- Each record includes: 
  - `customer_id` (unique identifier for the customer)
  - `month` (in YYYY-MM format)
  - `api_calls` (the number of API calls made that month)
- Example customer patterns include steadily increasing usage, decreasing usage, and irregular/spiky usage patterns.
- The data is grouped by customer, enabling trend analysis over time per customer.
