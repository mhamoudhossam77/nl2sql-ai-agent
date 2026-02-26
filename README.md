# Inventory Chatbot – NL2SQL AI Agent

An AI-powered inventory chatbot that converts natural language business questions into SQL queries, executes them on a real database, and returns both:
- the **final natural language answer**
- and the **exact SQL query used** (“present query”).

This project demonstrates how to safely combine **LLMs + Databases** for enterprise-style analytics use cases.

---

## 🚀 What This Project Does

Users can ask questions like:
- How many active assets do I have?
- How many assets by site?
- Total value of assets per site

The system will:
1. Convert the question to SQL using an LLM
2. Execute the SQL on the inventory database
3. Generate a human-readable answer
4. Return the SQL query for transparency

---

## 🧠 System Architecture (High Level)

Natural Language Question  
→ LLM (NL → SQL)  
→ Database Execution (SQLite)  
→ LLM (SQL Result → Answer)  
→ API Response  

The **database is the source of truth**.  
The LLM does NOT invent numbers — it only generates SQL and explains results.

---

## 🧱 Tech Stack

- Python 3.10+
- FastAPI
- SQLite (local database)
- OpenAI API (or Azure OpenAI)
- Pydantic
- dotenv

---

## 📂 Project Structure
