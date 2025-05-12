import streamlit as st
import os
from dotenv import load_dotenv
from main import query

# Load API key from .env (for LangChain/OpenAI use)
load_dotenv()

# Page title
st.title("💬 Sunrise Realty Q&A Assistant")
chat_placeholder = st.empty()

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

def start_chat():
    # Display chat messages from history
    with chat_placeholder.container():
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Get user input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user input to history and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response and display
        response = query(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        # Save assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    init_chat_history()
    start_chat()
