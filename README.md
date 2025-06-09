# 🧠 NL2SQL Streamlit App

Ask natural language questions and get answers from your database — no SQL knowledge required!

This app uses the **DeepSeek LLM** (via [OpenRouter](https://openrouter.ai)), **SQLite** for local structured data, and **Streamlit** for an interactive user interface. You can ask questions like:

- "Show all employees over 30"
- "What is the average salary by department?"
- "List names and ages of employees in Marketing"

---

## 🚀 Features

- 🔍 Natural language to SQL using DeepSeek LLM
- 🗃️ Query a local SQLite database
- 📊 Interactive chart generation from query results
- ⚙️ Configurable and extendable architecture

---

## 📦 Requirements

- Python 3.8+
- Free [OpenRouter](https://openrouter.ai) API key
- A local SQLite database (`my_database.db`) with at least one table

---

## 🛠️ Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/nl2sql-streamlit-app.git
cd nl2sql-streamlit-app
