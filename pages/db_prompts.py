import streamlit as st
from db.db import DatabaseHandler

# Instanciation de la base de données
db = DatabaseHandler()


# Vue Streamlit
st.subheader("Modifier un enregistrement dans la base de données")


# Vérification des éléments en session pour le type et la structure
if "type" in st.session_state and "structure" in st.session_state:

    # Récupération des valeurs en session
    session_type = st.session_state["type"]
    session_structure = st.session_state["structure"]

    # Chargement de l'enregistrement correspondant aux filtres
    selected_prompt = db.get_prompt_by_filters(session_type, session_structure)


    if selected_prompt:
        prompt_id, current_type, current_structure, current_prompt = selected_prompt


        # Champ pour le prompt
        new_prompt = st.text_area("", current_prompt)

        # Bouton pour sauvegarder les modifications
        if st.button("Sauvegarder les modifications"):
            db.update_prompt(prompt_id, current_type, current_structure, new_prompt)
            st.success("Les modifications ont été enregistrées.")

    else:
        st.warning("Aucun enregistrement trouvé avec les filtres actuels.")
else:
    st.warning("Les informations 'type' et 'structure' ne sont pas disponibles dans la session.")