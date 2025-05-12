## Project : Build a Custom Q&A Chatbot with OpenAI, LangChain, Chroma and Streamlit

## 💻 Project Overview

How to build a custom Q&A chatbot using OpenAI, LangChain, and Chroma.  
The OpenAI API generates answers to questions, LangChain translates the questions and answers to and from English, and Chroma.  

<!-- This section describes the Python setup using Python 3.12.9 -->

## 🛠️ Requirements : Installation & Setup

### Python 3.12.9

```bash
brew install pyenv
pyenv install 3.12.9
pyenv local 3.12.9
```

### Packages

- **LangChain** : [LangChain](https://www.langchain.com/) is a Python library for building LLM-powered applications.
- **Chroma** : [Chroma](https://www.trychroma.com/) is a vector database.
- **OpenAI** : [OpenAI](https://platform.openai.com) API interface.
- **python-dotenv** : Loads environment variables from a `.env` file.
- **Streamlit** : For building the web UI.

<!-- Removed streamlit-chat as it’s deprecated in favor of st.chat_message -->

## 🌐 Create a virtual environment & activate the virtual environment :

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

## 🏗️ Installation

```bash
pip install -r requirements.txt
```

<!-- Optional: Only use if testing with the latest LangChain releases -->
<!-- pip install --upgrade langchain -->

## 🔑 Get your OpenAI API key

[Generate API Key](https://platform.openai.com/account/api-keys)

Set the key as an environment variable:

```bash
export OPENAI_API_KEY='sk-...'
```

Or create a `.env` file :

```
OPENAI_API_KEY=sk-...
```
Or update and use example `.env.example` file.
```
cp .env.example .env
```
## ▶️ Run the app (command line interface)

```bash
python main.py
```

## ▶️ Run the Streamlit app (browser UI on localhost:8501)

```bash
streamlit run app.py
```
## ▶️ Run the Streamlit app without model selector (browser UI on localhost:8501)

```bash
streamlit run app-nb.py
```

---

## 🐳 Running with Docker

### Build the Docker image
```bash
docker build -t custom-chatbot-cli .
```

### Run the chatbot in CLI mode
```bash
docker run -it --rm --env-file .env custom-chatbot-cli
```

---

## 🧩 Running with Docker Compose

### Start the application
```bash
docker-compose up --build
```

This loads environment variables from `.env` and mounts source files. To rebuild with changes:
```bash
docker-compose up --build --force-recreate
```

---

### Notes
- Make sure your `.env` file contains a valid OpenAI API key.
- Ensure `docs/` includes your `.txt` knowledge files (e.g., `faq_real_estate.txt`).
- Local Python environments (`env/`) are excluded via `.dockerignore`.

---

## ✅ How to Use

Place the `docker-compose.yml` file at the root of your project.

### Run the CLI chatbot:
```bash
docker compose run chatbot-cli
```

### Run the Streamlit web app:
```bash
docker compose up chatbot-ui
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.
