import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Model config from .env or fallback
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL", "gpt-3.5-turbo")

model = ChatOpenAI(model_name=LANGUAGE_MODEL)

# Prompt Templates
template = (
    "You are a knowledgeable and friendly real estate assistant at Sunrise Realty Group.\n"
    "You help clients with questions about buying, selling, and renting homes.\n"
    "Use only the following information to answer clearly and professionally:\n"
    "{context}"
)
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# Chroma-compatible wrapper for embedding function
class ChromaEmbeddingWrapper:
    def __init__(self):
        self._embedder = OpenAIEmbeddings()

    def __call__(self, input):
        return self._embedder.embed_documents(input)

    def embed_documents(self, texts):
        return self._embedder.embed_documents(texts)

    def embed_query(self, text):
        return self._embedder.embed_query(text)

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def load_documents():
    """Loads and splits documents from the ./docs directory."""
    raw_documents = TextLoader("./docs/faq_real_estate.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_documents(raw_documents)

def load_embeddings(documents, user_query):
    """Embeds and loads documents into Chroma vector store with compliant wrapper."""
    embedding_function = ChromaEmbeddingWrapper()
    db = Chroma.from_documents(
        documents,
        embedding=embedding_function,
        collection_name="abc-faq"
    )
    return db.as_retriever()

def generate_response(retriever, query):
    """Generates a response using retrieval-augmented generation."""
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)

def query(query_text, model_name=None):
    """High-level query function used by app.py or CLI."""
    global model
    if model_name:
       model = ChatOpenAI(model_name=model_name)

    documents = load_documents()
    retriever = load_embeddings(documents, query_text)
    response = generate_response(retriever, query_text)
    return response

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