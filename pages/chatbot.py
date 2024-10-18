import streamlit as st
import yaml
import os
from streamlit_chat import message
from model import selector

def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


# Charger les données YAML
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def process_input():
    if "user_input" in st.session_state and st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()

        with st.session_state["thinking_spinner"], st.spinner(f"Je réfléchis"):
            agent_text = st.session_state["assistant"].ask(user_text, st.session_state["messages"] if "messages" in st.session_state else [], variables=st.session_state["data_dict"])

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

@st.dialog("Choisissez votre prompt")
def show_prompts():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    yaml_data = load_yaml(file_path)
        
        # Boucle à travers les éléments YAML
    for categroy in yaml_data['prompts']:  # Exemple avec la catégorie conversation
        st.write(categroy.capitalize())

        for item in yaml_data['prompts'][categroy]:
            if st.button(item, key=f"button_{item}"):
                st.session_state["user_input"] = item
                st.rerun()

def page():
    st.subheader("Posez vos questions")

    if "user_input" in st.session_state:
        process_input()

    if "assistant" not in st.session_state:
        st.text("Assistant non initialisé")
    
    # Bouton pour ouvrir la modale
    if st.button("Prompts pré-définis"):
        show_prompts()


    selector.ModelSelector()

    # Get prompt system
    # prompt_sys = st.session_state.prompt_system if 'prompt_system' in st.session_state and st.session_state.prompt_system != '' else "Renseignez votre prompt system"
    
    display_messages()

    st.text_input("Message", key="user_input", on_change=process_input)

page()