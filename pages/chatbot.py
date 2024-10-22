import streamlit as st
from streamlit_chat import message
from model import selector
from util import getYamlConfig


def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if "user_input" in st.session_state and st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()

        prompt_sys = st.session_state.prompt_system if 'prompt_system' in st.session_state and st.session_state.prompt_system != '' else ""
    
        with st.session_state["thinking_spinner"], st.spinner(f"Je réfléchis"):
            agent_text = st.session_state["assistant"].ask(user_text, prompt_system=prompt_sys, messages=st.session_state["messages"] if "messages" in st.session_state else [], variables=st.session_state["data_dict"])
            
        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))
        st.session_state["user_input"] = ""


def show_prompts():
    yaml_data = getYamlConfig()["prompts"]
    
    expander = st.expander("Prompts pré-définis")
    
    for categroy in yaml_data:
        expander.write(categroy.capitalize())

        for item in yaml_data[categroy]:
            if expander.button(item, key=f"button_{item}"):
                st.session_state["user_input"] = item
                process_input()


def page():
    st.subheader("Posez vos questions")

    if "user_input" in st.session_state:
        process_input()

    if "assistant" not in st.session_state:
        st.text("Assistant non initialisé")

    # Collpase for default prompts
    show_prompts()

    # Models selector
    selector.ModelSelector()
    
    # Displaying messages
    display_messages()

    # Input user query
    st.text_input("Message", key="user_input", on_change=process_input)


page()