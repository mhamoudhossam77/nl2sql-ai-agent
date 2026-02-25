import time
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from llm_service import LLMService
from database import get_connection

app = FastAPI()
llm_service = LLMService()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    natural_language_answer: str
    sql_query: str
    token_usage: TokenUsage
    latency_ms: int
    provider: str
    model: str
    status: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    start_time = time.time()
    try:
        # 1. Generate SQL from natural language
        sql_query, sql_usage = llm_service.generate_sql(request.message)

        # 2. Execute SQL query
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            sql_result = [dict(zip(columns, row)) for row in rows]
            conn.close()
        except Exception as db_err:
            # Fallback if SQL is invalid or execution fails
            sql_result = f"Error executing SQL: {str(db_err)}"

        # 3. Generate natural language answer from SQL result
        answer, answer_usage = llm_service.generate_answer(
            request.message, sql_query, sql_result
        )

        total_latency = int((time.time() - start_time) * 1000)

        total_usage = {
            "prompt_tokens": sql_usage["prompt_tokens"] + answer_usage["prompt_tokens"],
            "completion_tokens": sql_usage["completion_tokens"] + answer_usage["completion_tokens"],
            "total_tokens": sql_usage["total_tokens"] + answer_usage["total_tokens"]
        }

        return ChatResponse(
            natural_language_answer=answer,
            sql_query=sql_query,
            token_usage=TokenUsage(**total_usage),
            latency_ms=total_latency,
            provider=llm_service.provider,
            model=llm_service.model_name,
            status="ok"
        )

    except Exception as e:
        total_latency = int((time.time() - start_time) * 1000)
        return ChatResponse(
            natural_language_answer=f"An error occurred: {str(e)}",
            sql_query="",
            token_usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            latency_ms=total_latency,
            provider=llm_service.provider,
            model=llm_service.model_name,
            status="error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
