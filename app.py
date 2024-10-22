import streamlit as st
import os

from dotenv import load_dotenv
from rag import Rag
from vectore_store.PineconeConnector import PineconeConnector
from vectore_store.VectoreStoreManager import VectoreStoreManager

from util import getYamlConfig

load_dotenv()

GROUP_NAME = os.environ.get("APP_NAME")
LOGO = "assets/logo.png"

def init_app():

    config = getYamlConfig()

    if len(st.session_state) == 0:
        # Define Vectore store strategy
        pinecone_connector = PineconeConnector()
        vs_manager = VectoreStoreManager(pinecone_connector)

        st.session_state["messages"] = []
        st.session_state["assistant"] = Rag(vectore_store=vs_manager)
        st.session_state["data_dict"] = config['variables']
        st.session_state["prompt_system"] = config['prompt_system']


def main():

    init_app()

    st.set_page_config(page_title=GROUP_NAME)

    st.logo(LOGO)
    st.title(GROUP_NAME)

    saved_documents = st.Page("pages/persistent_documents.py", title="Communs", icon="🗃️")
    documents = st.Page("pages/documents.py", title="Vos documents", icon="📂")
    prompt_system = st.Page("pages/prompt_system.py", title="Prompt système", icon="🖊️", default=True)
    form = st.Page("pages/form.py", title="Paramètres", icon="📋")
    chatbot = st.Page("pages/chatbot.py", title="Chatbot", icon="🤖")

    pg = st.navigation(
        {
            "Documents": [
                saved_documents,
                documents,
            ],
            "Configurations": [
                prompt_system,
                form,
            ],
            "Dialogue": [
                chatbot
            ],
        }
    )

    pg.run()


if __name__ == "__main__":
    main()