import os
import tempfile
import streamlit as st

def uploadToDb():

    for file in st.session_state["file_uploader_commun"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Chargement {file.name}"):
            st.session_state["assistant"].ingestToDb(file_path, filename=file.name)
        os.remove(file_path)

def page():
    st.subheader("Montez des documents communs")
    
    st.file_uploader(
        "Télécharger un documents",
        type=["pdf"],
        key="file_uploader_commun",
        accept_multiple_files=True,
        on_change=uploadToDb,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    st.divider()
    st.write("Documents dans la base de données")
    
    for doc in st.session_state["assistant"].vector_store.getDocs():
        st.write(" - "+doc)
    
page()