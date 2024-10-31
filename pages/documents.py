import os
import tempfile
import streamlit as st

def read_and_save_file():
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Chargement {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)



def page():
    st.subheader("Charger vos documents")

    # File uploader
    uploaded_file = st.file_uploader(
        "Télécharger un ou plusieurs documents",
        type=["pdf"],
        key="file_uploader",
        accept_multiple_files=True,
        on_change=read_and_save_file,
    )


    st.session_state["ingestion_spinner"] = st.empty()


    for doc in st.session_state["assistant"].list_documents():
        st.write(doc)

page()