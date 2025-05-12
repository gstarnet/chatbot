# 🔍 Custom Knowledge Chatbot

## 🧠 Project Summary

This updated **Custom Knowledge Chatbot** enables dynamic question-answering from custom text files (e.g., FAQs, internal docs) using **OpenAI’s GPT models**, **LangChain**, and **ChromaDB**. The application is designed to run both as a **CLI chatbot** and a **Streamlit-based web interface**, with seamless deployment via **Docker** and **Docker Compose**.

---

## ⚙️ Technology Stack

| Component          | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **LangChain**      | Manages retrieval-augmented generation and interaction with LLMs.       |
| **OpenAI API**     | Powers natural language understanding and answer generation.            |
| **ChromaDB**       | Embedding-based vector store for fast document similarity search.       |
| **Streamlit**      | Web-based UI for interactive question-answer flow.                      |
| **Docker**         | Creates portable, self-contained development and deployment images.     |
| **Docker Compose** | Manages services and configuration for CLI and web app simultaneously.  |

---

## 🧱 Architecture & Workflow

1. **Document Ingestion**:  
   Text files in the `docs/` directory (e.g., `faq_real_estate.txt`) are parsed and embedded into a vector store using `Chroma` + `OpenAIEmbeddings`.

2. **Query Handling**:  
   User queries are transformed into vectors. The most relevant documents are retrieved via similarity search.

3. **LLM Response Generation**:  
   LangChain invokes `ChatOpenAI` to generate context-aware answers using the top-matching documents as prompt context.

4. **Interface Modes**:
   - **Command-line**: Lightweight CLI chatbot via `main.py`.
   - **Web app**: Streamlit frontend (with/without model selector) via `app.py` or `app-nb.py`.

---

## 🚀 Real-World Use Case Scenarios

This framework can be adapted to multiple real-world applications:

### 🏢 Internal Knowledge Assistant
- Index company policy manuals or HR guidelines.
- Employees can query docs using natural language.

### 🎓 Educational Helpdesk
- Train the model on course material or lecture notes.
- Students ask questions and get tutor-like answers.

### 🛒 E-commerce FAQ Bot
- Feed it product documentation or FAQ sheets.
- Enables automated support across platforms.

### ⚖️ Legal/Compliance Reference Tool
- Use internal compliance manuals.
- Responds with citations to legal clauses and rulings.

---

## 🛠️ Customization Potential

- **Swap Embedding Model**: Replace OpenAI with Hugging Face or Cohere.
- **Multi-language Support**: Add translation with DeepL or Google Translate APIs.
- **Multi-user Authentication**: Use Streamlit authentication or container-level restrictions.
- **Chat History Storage**: Extend CLI/Streamlit app to log conversations in SQLite or Supabase.

---

## 📦 Deployment & DevOps Enhancements

- The `.env` file securely handles your `OPENAI_API_KEY`.
- `.dockerignore` ensures only necessary files are shipped into the container (excluding `env/`, `.idea/`, `__pycache__/`).
- Docker Compose spins up both CLI and Web UI using:

```bash
docker compose run chatbot-cli       # CLI
docker compose up chatbot-ui         # Web UI at http://localhost:8501
```
