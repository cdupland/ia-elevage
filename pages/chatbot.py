import streamlit as st
from streamlit_chat import message
from model import selector

def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()


        with st.session_state["thinking_spinner"], st.spinner(f"Je réfléchis"):
            agent_text = st.session_state["assistant"].ask(user_text, st.session_state["messages"] if "messages" in st.session_state else [], variables=st.session_state["data_dict"])

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def page():
    st.subheader("Posez vos questions")

    selector.ModelSelector()

    if "assistant" not in st.session_state:
        st.text("Assistant non initialisé")


    prompt_sys = st.session_state.prompt_system if 'prompt_system' in st.session_state and st.session_state.prompt_system != '' else "Renseignez votre prompt system"

    st.text("Prompt system : " + prompt_sys)

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

page()