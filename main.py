from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sqlite3
import requests
import os

# Load .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Allow frontend (Streamlit or others) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class QuestionRequest(BaseModel):
    question: str

# Function to convert natural language to SQL using OpenRouter
def ask_openrouter(question: str) -> str:
    schema_hint = """
You are an assistant that generates SQL queries for a SQLite database with this schema:

Table: employees
- id (INTEGER)
- name (TEXT)
- age (INTEGER)
- department (TEXT)
- salary (REAL)

Only respond with the SQL query. Do not include explanations.
"""
    prompt = f"{schema_hint}\n\nQuestion: {question}"

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 500
        }
    )

    data = response.json()
    if "choices" not in data:
        raise ValueError(f"Failed to get SQL from OpenRouter: {data}")
    
    # Extract and clean SQL response
    raw_sql = data["choices"][0]["message"]["content"].strip()
    cleaned_sql = (
        raw_sql.replace("```sql", "")
               .replace("```", "")
               .strip()
    )
    return cleaned_sql
    

# API endpoint to handle the question
@app.post("/ask")
def ask(request: QuestionRequest):
    sql = ask_openrouter(request.question)

    try:
        # Connect to your SQLite DB
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        conn.close()

        return {
            "sql": sql,
            "columns": columns,
            "rows": rows
        }
    except Exception as e:
        return {
            "error": str(e),
            "sql": sql
        }

