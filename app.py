import streamlit as st
import os

from dotenv import load_dotenv
from rag import Rag
from vectore_store.PineconeConnector import PineconeConnector
from vectore_store.VectoreStoreManager import VectoreStoreManager


load_dotenv()

GROUP_NAME = os.environ.get("APP_NAME")

def init_app():
    
    # Read the environment variable and create a dictionary
    variables = os.environ.get('VARIABLES')
    keys = variables.split(',')
    data_dict = {key: '' for key in keys}  # Initialize with empty values

    if len(st.session_state) == 0:
        # Define Vectore store strategy
        pinecone_connector = PineconeConnector()
        vs_manager = VectoreStoreManager(pinecone_connector)

        st.session_state["messages"] = []
        st.session_state["assistant"] = Rag(vectore_store=vs_manager)
        st.session_state["data_dict"] = data_dict


def main():

    init_app()

    st.set_page_config(page_title=GROUP_NAME)

    st.title(GROUP_NAME)

    prompt_system = st.Page("pages/prompt_system.py", title="Prompt système", icon="📋", default=True)
    saved_documents = st.Page("pages/persistent_documents.py", title="Documents Communs", icon="📋")
    documents = st.Page("pages/documents.py", title="Documents", icon="📋")
    form = st.Page("pages/form.py", title="Formulaire", icon="📋")
    chatbot = st.Page("pages/chatbot.py", title="Chatbot", icon="📋")

    pg = st.navigation(
        [
            saved_documents,
            prompt_system,
            documents,
            form,
            chatbot
        ]
    )

    pg.run()


if __name__ == "__main__":
    main()