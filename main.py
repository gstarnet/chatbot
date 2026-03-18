import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_community.retrievers import BM25Retriever
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL", "gemma3:4b")


class ChatbotRuntimeError(RuntimeError):
    """Raised when the local model runtime is unavailable."""

# Prompt Templates
template = (
    "You are a knowledgeable and friendly real estate assistant at Sunrise Realty Group.\n"
    "You help clients with questions about buying, selling, and renting homes.\n"
    "Use only the information provided in the context to answer clearly and professionally.\n"
    "If the question cannot be answered from the context or is unrelated to real estate, reply with:"
    " 'I'm sorry, but I don't have information about that based on the provided materials.'\n"
    "Do not introduce or reference characters, events, or facts that are not explicitly supported by the context.\n"
    "Context:\n"
    "{context}"
)
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def load_documents():
    """Loads and splits documents from the ./docs directory."""
    raw_documents = TextLoader("./docs/faq_real_estate.txt").load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )
    return text_splitter.split_documents(raw_documents)

def load_retriever(documents):
    """Creates a lightweight keyword retriever for the local FAQ corpus."""
    retriever = BM25Retriever.from_documents(documents)
    retriever.k = 4
    return retriever

def generate_response(retriever, query, model_name):
    """Generates a response using retrieval-augmented generation."""
    model = ChatOllama(
        model=model_name,
        base_url=OLLAMA_BASE_URL,
        temperature=0.2,
    )
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)

def query(query_text, model_name=None):
    """High-level query function used by app.py or CLI."""
    current_model = model_name or LANGUAGE_MODEL

    try:
        documents = load_documents()
        retriever = load_retriever(documents)
        response = generate_response(retriever, query_text, current_model)
        return response
    except Exception as exc:
        message = str(exc)
        if "model failed to load" in message:
            raise ChatbotRuntimeError(
                "Ollama could not load the requested local model. "
                f"Chat model: {current_model}. "
                "This usually means the Ollama server is out of available memory or is in a bad state. "
                "Try `ollama ps`, restart the Ollama server, or switch to a smaller chat model."
            ) from exc
        if "Failed to connect" in message or "could not connect" in message.lower():
            raise ChatbotRuntimeError(
                "The app could not reach the Ollama server. "
                f"Expected server: {OLLAMA_BASE_URL}. "
                "Make sure `ollama serve` is running."
            ) from exc
        raise

# CLI entrypoint
if __name__ == "__main__":
    try:
        while True:
            user_input = input("\nAsk a question (or type 'exit' to quit): ")
            if user_input.strip().lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            answer = query(user_input)
            print("\n🧠 Response:")
            print(answer)
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")
