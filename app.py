import streamlit as st
import os

from dotenv import load_dotenv
from rag import Rag
from vectore_store.PineconeConnector import PineconeConnector
from vectore_store.VectoreStoreManager import VectoreStoreManager
from db.db import DatabaseHandler

from util import getYamlConfig

load_dotenv()

GROUP_NAME = os.environ.get("APP_NAME")
LOGO = "assets/logo.png"

def init_app():
    # Instanciation de la base de données
    db = DatabaseHandler()

    config = getYamlConfig()

    if len(st.session_state) == 0:
        # Define Vectore store strategy
        pinecone_connector = PineconeConnector()
        vs_manager = VectoreStoreManager(pinecone_connector)

        st.session_state["messages"] = []
        st.session_state["assistant"] = Rag(vectore_store=vs_manager)
        st.session_state["data_dict"] = config['variables']
        st.session_state["prompt_system"] = config['prompt_system']

        if 'parts' in config['variables']:
            # Flatten structure by adding part name to each field
            st.session_state["data_dict"] = [
                {**field, "part": part["name"]}
                for part in config["variables"]["parts"]
                for field in part["fields"]
            ]
        else:
            # Initialize session state with single list of variables
            st.session_state["data_dict"] = [{**field} for field in config["variables"]]

def getStructure():
    
    if st.session_state.type == "beef_cattle":
        # Bovins Viande
        return {
            "Petite": "small",
            "GAEC": "gaec",
            "GAEC Bis": "gaec_bis",
        }
    
    elif st.session_state.type == "dairy_cattle":
        # Bovins Lait
        return {
            "Petite": "small",
            "Moyenne": "medium",
            "Hors zone": "out"
        }
    
    
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

    db_prompts = st.Page("pages/db_prompts.py", title="Prompt Template", icon="📋")

    pg = st.navigation(
        {
            "Documents": [
                saved_documents,
                documents,
            ],
            "Configurations": [
                prompt_system,
                form,
                db_prompts
            ],
            "Dialogue": [
                chatbot
            ],
        },
        expanded=True
    )

    with st.sidebar:
        st.write("**Configuration**")


        # Type
        type_options = {
            "Bovins Viande": "beef_cattle",
            "Bovins Lait": "dairy_cattle"
        }
        selected_type_label = st.radio("Type", list(type_options.keys()))
        st.session_state["type"] = type_options[selected_type_label]


        # Structure
        structure_options = getStructure()
        selected_structure_label = st.selectbox("Structure", list(structure_options.keys()))
        st.session_state["structure"] = structure_options[selected_structure_label]

    pg.run()


if __name__ == "__main__":
    main()