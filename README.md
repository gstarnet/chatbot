# 🧠 Project: Custom Knowledge Q&A Chatbot

## 💻 Project Overview

How to build a custom Q&A chatbot using OpenAI, LangChain, and Chroma.  
The OpenAI API generates answers to questions, LangChain handles prompt construction and retrieval, and ChromaDB serves as a vector database to search relevant content chunks.

---

## 🛠️ Requirements: Installation & Setup

### Python 3.12.9

```bash
brew install pyenv
pyenv install 3.12.9
pyenv local 3.12.9
```

### Python Packages

Installed via `requirements.txt`:

- **LangChain**: Framework to interface with LLMs and orchestrate prompt chaining.
- **Chroma**: Lightweight vector database for fast retrieval.
- **OpenAI**: Language model and embedding API.
- **python-dotenv**: Loads environment variables.
- **Streamlit**: Interactive UI framework.
- **Others**: `tiktoken`, `colorama`, `requests`, `dateutil`.

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

---

## 🔑 API Key

Get your key from [OpenAI](https://platform.openai.com/account/api-keys)

Set it via environment variable:

```bash
export OPENAI_API_KEY='sk-...'
```

Or store in a `.env` file:

```
OPENAI_API_KEY=sk-...
```

Or duplicate template:

```bash
cp .env.example .env
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
| **OpenAI API**     | Provides natural language understanding and embedding generation.       |
| **ChromaDB**       | Stores document embeddings for similarity search.                       |
| **Streamlit**      | Builds a user-friendly, interactive web interface.                      |
| **Docker**         | Containers for environment consistency and ease of deployment.          |
| **Docker Compose** | Orchestrates CLI and UI services simultaneously with shared config.     |
| **dotenv**         | Loads and manages API keys securely in local development.               |

---
## 🧱 Architecture Summary

1. **Document Ingestion**
    - Raw text (`faq_real_estate.txt`) is loaded and split into 100-character chunks using `CharacterTextSplitter`.

2. **Embedding & Vector Storage**
    - Chunks are embedded using `OpenAIEmbeddings` and stored in a ChromaDB vector store.

3. **Query Flow**
    - User questions are embedded, compared to stored chunks for similarity, and the top matches are passed as **context**.

4. **Prompt Assembly & LLM Output**
    - LangChain constructs a system + human prompt using the retrieved context and sends it to OpenAI’s chat model.

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
text_splitter = CharacterTextSplitter(chunk_size=100)
documents = text_splitter.split_documents(raw_documents)
```

### Embedding & Chroma Vector Store

```python
embedding_function = OpenAIEmbeddings()
db = Chroma.from_documents(documents, embedding_function)
retriever = db.as_retriever()
```

### Prompt & Chain with LangChain

```python
template = (
    "You are a knowledgeable assistant. Use the following info:\n{context}"
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
    | ChatOpenAI(...)
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
- ✅ Modify vector store to use alternatives like FAISS or Weaviate for scale.
- ✅ Replace `OpenAIEmbeddings` with Hugging Face or Cohere embeddings.
- ✅ Store chat history with SQLite or connect Streamlit to Supabase for persistence.

---
