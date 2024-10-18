import streamlit as st

def page():

    st.subheader("Renseignez votre prompt système")

    prompt = st.text_area("Prompt system", st.session_state.prompt_system if 'prompt_system' in st.session_state else "")

    # Session State also supports attribute based syntax
    st.session_state['prompt_system'] = prompt

page()