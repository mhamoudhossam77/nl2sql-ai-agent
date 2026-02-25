import os
import time
from typing import Dict, Any, Tuple
from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.provider = os.getenv("PROVIDER", "openai").lower()
        self.api_key = os.getenv("MODEL_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4")

        if not self.api_key or self.api_key == "mock":
            self.client = None
        elif self.provider == "azure":
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version="2023-05-15",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
        else:
            self.client = OpenAI(api_key=self.api_key)

    def _call_llm(self, messages: list) -> Tuple[str, Dict[str, int]]:
        if self.client is None:
            # Mock implementation for testing without API keys
            user_content = messages[-1]["content"]
            if "SQL Result" in user_content:
                # This is the answer generation part
                result_part = user_content.split("SQL Result: ")[1].split("\n")[0].strip()
                return f"Based on the results: {result_part}, the final answer is provided.", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

            if "how many assets" in user_content.lower():
                if "by site" in user_content.lower():
                    return "SELECT s.SiteName, COUNT(*) AS AssetCount FROM Assets a JOIN Sites s ON s.SiteId = a.SiteId WHERE a.Status <> 'Disposed' GROUP BY s.SiteName ORDER BY AssetCount DESC;", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                return "SELECT COUNT(*) AS AssetCount FROM Assets WHERE Status <> 'Disposed';", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            if "total value" in user_content.lower():
                return "SELECT s.SiteName, SUM(a.Cost) AS TotalValue FROM Assets a JOIN Sites s ON s.SiteId = a.SiteId WHERE a.Status <> 'Disposed' GROUP BY s.SiteName;", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            return "SELECT * FROM Assets LIMIT 5;", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return content, usage

    def generate_sql(self, user_query: str) -> Tuple[str, Dict[str, int]]:
        system_prompt = """
You are a SQL Server expert. Given the following database schema, generate a SQL query to answer the user's question.
Return ONLY the SQL query. No markdown formatting.

Schema:
- Customers (CustomerId, CustomerCode, CustomerName, Email, Phone, BillingAddress1, BillingCity, BillingCountry, CreatedAt, UpdatedAt, IsActive)
- Vendors (VendorId, VendorCode, VendorName, Email, Phone, AddressLine1, City, Country, CreatedAt, UpdatedAt, IsActive)
- Sites (SiteId, SiteCode, SiteName, AddressLine1, City, Country, TimeZone, CreatedAt, UpdatedAt, IsActive)
- Locations (LocationId, SiteId, LocationCode, LocationName, ParentLocationId, CreatedAt, UpdatedAt, IsActive)
- Items (ItemId, ItemCode, ItemName, Category, UnitOfMeasure, CreatedAt, UpdatedAt, IsActive)
- Assets (AssetId, AssetTag, AssetName, SiteId, LocationId, SerialNumber, Category, Status, Cost, PurchaseDate, VendorId, CreatedAt, UpdatedAt)
- Bills (BillId, VendorId, BillNumber, BillDate, DueDate, TotalAmount, Currency, Status, CreatedAt, UpdatedAt)
- PurchaseOrders (POId, PONumber, VendorId, PODate, Status, SiteId, CreatedAt, UpdatedAt)
- PurchaseOrderLines (POLineId, POId, LineNumber, ItemId, ItemCode, Description, Quantity, UnitPrice)
- SalesOrders (SOId, SONumber, CustomerId, SODate, Status, SiteId, CreatedAt, UpdatedAt)
- SalesOrderLines (SOLineId, SOId, LineNumber, ItemId, ItemCode, Description, Quantity, UnitPrice)
- AssetTransactions (AssetTxnId, AssetId, FromLocationId, ToLocationId, TxnType, Quantity, TxnDate, Note)

Rules:
1. Use SQL Server syntax.
2. For "how many assets", filter by Status <> 'Disposed'.
3. Always use JOINs where necessary.
4. Return ONLY the SQL string. No markdown, no triple backticks.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        return self._call_llm(messages)

    def generate_answer(self, user_query: str, sql_query: str, sql_result: Any) -> Tuple[str, Dict[str, int]]:
        system_prompt = "You are a helpful business assistant. Use the provided SQL result to answer the user's question naturally."
        user_prompt = f"""
User Question: {user_query}
SQL Query: {sql_query}
SQL Result: {sql_result}

Provide a concise natural language answer based on the result.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self._call_llm(messages)
