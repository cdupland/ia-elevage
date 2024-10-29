import streamlit as st

def page():
    st.subheader("Définissez vos paramètres")

    # Boucle pour créer des inputs basés sur data_dict (qui est une liste ici)
    for param in st.session_state.data_dict:
        
        if param['nature'] == 'radio':
          value = st.radio(param['label'], param['options'], key=param['key'], args=[param['key']])
          param['value'] = value
        elif param['nature'] == 'selectbox':
          value = st.selectbox(param['label'], param['options'], key=param['key'], args=[param['key']])
          param['value'] = value
        elif param['nature'] == 'multiselect':
          value = st.multiselect(param['label'], param['options'], key=param['key'], args=[param['key']])
          param['value'] = value
        else:
          # Utilisation de la clé 'label' et 'value' pour afficher et récupérer les valeurs
          value = st.text_input(label=param['label'], value=param['value'] if param['value'] else "")
          # Mettre à jour la valeur dans le dictionnaire après la saisie utilisateur
          param['value'] = value

page()