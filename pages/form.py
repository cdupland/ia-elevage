import streamlit as st

def page():
    st.subheader("Définissez vos paramètres")

    for key in st.session_state.data_dict.keys():
        value = st.text_input(label=key, value=st.session_state.data_dict[key])
        st.session_state.data_dict[key] = value  # Update the session state with user input

page()