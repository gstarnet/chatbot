# 🧠 Project: Custom Knowledge Q&A Chatbot

## 💻 Project Overview

How to build a custom Q&A chatbot using Ollama, LangChain, and Streamlit.  
A local Ollama server generates answers, LangChain handles prompt construction and retrieval, and a lightweight BM25 retriever keeps the FAQ search local and Python 3.14-compatible. The assistant is tuned for Sunrise Realty Group and answers only from the supplied real-estate FAQ context.

---

## 🛠️ Requirements: Installation & Setup

### Python 3.14.3

```bash
brew install pyenv
pyenv install 3.14.3
pyenv local 3.14.3
```

### Python Packages

Installed via `requirements.txt`:

- **LangChain**: Framework to interface with LLMs and orchestrate prompt chaining.
- **Ollama**: Local language model and embedding runtime.
- **BM25**: Lightweight keyword-based retrieval over the local FAQ content.
- **python-dotenv**: Loads environment variables.
- **Streamlit**: Interactive UI framework.
- **watchdog**: Improves Streamlit file watching and local dev responsiveness.
- **Others**: `colorama`, `requests`, `dateutil`.

---

## 🌐 Virtual Environment Setup

**MacOS/Linux**:

```bash
python3 -m venv env
source env/bin/activate
```

**Windows**:

```bash
python -m venv env
env\Scripts\activate
```

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

If you already have an older virtualenv, recreate it after switching Python versions:

```bash
rm -rf env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

## 🤖 Ollama Setup

Make sure your local Ollama server is running and the required models are already available:

```bash
ollama serve
ollama pull gemma3:4b
```

Then duplicate the template:

```bash
cp .env.example .env
```

Default `.env` values:

```bash
OLLAMA_BASE_URL=http://localhost:11434
LANGUAGE_MODEL=gemma3:4b
```

---

## ▶️ Run the Application

### CLI Mode

```bash
python main.py
```

### Web UI (Streamlit)

```bash
streamlit run app.py
```

Alternative (minimalist UI):

```bash
streamlit run app-nb.py
```

Then open [http://localhost:8501](http://localhost:8501)

---

## ⚙️ Technology Stack

| Component          | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **LangChain**      | Manages prompt templates, chaining, and LLM interactions.               |
| **Ollama**         | Serves the local chat model.                                            |
| **BM25Retriever**  | Retrieves relevant FAQ chunks without loading an embedding model.       |
| **Streamlit**      | Builds a user-friendly, interactive web interface.                      |
| **Docker**         | Containers for environment consistency and ease of deployment.          |
| **Docker Compose** | Orchestrates CLI and UI services simultaneously with shared config.     |
| **dotenv**         | Loads and manages API keys securely in local development.               |

---
## 🧱 Architecture Summary

1. **Document Ingestion**
    - Raw text (`faq_real_estate.txt`) is loaded and split with `RecursiveCharacterTextSplitter` into overlapping chunks for retrieval.

2. **Retrieval**
    - Chunks are indexed with a BM25 retriever for fast local keyword search without loading a separate embedding model.

3. **Query Flow**
    - User questions are matched against the FAQ chunks, and the most relevant passages are passed as **context**.

4. **Prompt Assembly & LLM Output**
    - LangChain constructs a system + human prompt that tells the assistant to act as a Sunrise Realty Group real-estate assistant, stay grounded in the provided context, and refuse unsupported or unrelated questions.

5. **Response Output**
    - The chatbot returns a refined, context-aware response through CLI or Streamlit UI.

---

## 📁 Source Structure

```
.
├── app.py              # Streamlit app (model selector)
├── app-nb.py           # Streamlit app (simplified)
├── main.py             # CLI chatbot + core logic
├── Dockerfile
├── docker-compose.yml
├── docs/
│   └── faq_real_estate.txt
├── requirements.txt
└── .env.example
```

---

## 🧠 Core Code Snippets

### Document Loading

```python
raw_documents = TextLoader("./docs/faq_real_estate.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
documents = text_splitter.split_documents(raw_documents)
```

### Retrieval

```python
retriever = BM25Retriever.from_documents(documents)
retriever.k = 4
```

### Prompt & Chain with LangChain

```python
template = (
    "You are a knowledgeable and friendly real estate assistant at Sunrise Realty Group.\n"
    "Use only the information provided in the context.\n"
    "If the question cannot be answered from the context or is unrelated to real estate, reply with:\n"
    "'I'm sorry, but I don't have information about that based on the provided materials.'\n"
    "Context:\n{context}"
)
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    HumanMessagePromptTemplate.from_template("{question}")
])
```

### Chain Execution

```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | chat_prompt
    | ChatOllama(model="gemma3:4b")
    | StrOutputParser()
)
response = chain.invoke("What are the closing costs?")
```

---

## 🐳 Docker Setup

### Build Image

```bash
docker build -t custom-chatbot-cli .
```

### Run CLI in Container

```bash
docker run -it --rm --env-file .env custom-chatbot-cli
```

---

## 🧩 Docker Compose (Preferred)

```bash
docker-compose up --build
```

For Docker Compose, the app containers default to `http://host.docker.internal:11434` so they can reach an Ollama server running on your host machine.

Rebuild with changes:

```bash
docker-compose up --build --force-recreate
```

---

## 🧼 Dockerignore Example

Make builds faster by ignoring:

```
env/
.idea/
__pycache__/
```

---

## ✅ Use Cases

- **Real Estate Agents** – e.g., Sunrise Realty FAQ bot
- **Internal Knowledgebase** – HR, IT support, SOPs
- **Legal/Compliance Q&A** – Clause-specific search
- **Education** – Course notes and FAQ retrieval

---

## 💡 Tips for Customization

- ✅ Swap out `faq_real_estate.txt` with any domain-specific `.txt` content in `docs/`.
- ✅ Update prompt template in `main.py` to reflect your brand tone.
- ✅ Replace BM25 with Chroma, FAISS, or Weaviate if you later want semantic search or persistence.
- ✅ Replace `OllamaEmbeddings` with another local or hosted embedding model if needed.
- ✅ Store chat history with SQLite or connect Streamlit to Supabase for persistence.

---
