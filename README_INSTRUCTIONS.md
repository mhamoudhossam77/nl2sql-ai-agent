# Inventory Chatbot API

This is a minimal AI chat service that answers inventory and business questions by converting natural language to SQL.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in a `.env` file:
   ```
   PROVIDER=openai
   MODEL_API_KEY=your_openai_api_key
   MODEL_NAME=gpt-4
   ```

3. Initialize the database:
   ```bash
   python seed_db.py
   ```

4. Run the API:
   ```bash
   uvicorn main:app --reload
   ```

## API Usage

### POST /api/chat

Request body:
```json
{
  "session_id": "123",
  "message": "How many assets do I have?",
  "context": {}
}
```

Response:
```json
{
  "natural_language_answer": "You have 3 assets in your inventory.",
  "sql_query": "SELECT COUNT(*) AS AssetCount FROM Assets WHERE Status <> 'Disposed';",
  "token_usage": {
    "prompt_tokens": 150,
    "completion_tokens": 20,
    "total_tokens": 170
  },
  "latency_ms": 1200,
  "provider": "openai",
  "model": "gpt-4",
  "status": "ok"
}
```

## Testing

Run the tests using:
```bash
python test_api.py
```
