import streamlit as st
from util import getYamlConfig

def page():
    st.subheader("Définissez vos paramètres")

    # Charge la configuration YAML
    config = getYamlConfig()
    
    # Vérifie si la structure inclut des 'parts' ou une liste de variables
    if 'parts' in config['variables']:
        # Cas avec 'parts' : Trie les parts et affiche les champs par onglet
        parts = config["variables"]["parts"]
        parts_sorted = sorted(parts, key=lambda part: part.get('number', float('inf')))
        
        # Création de tabs pour chaque 'part' trié
        tabs = st.tabs([part['name'] for part in parts_sorted])
        for part, tab in zip(parts_sorted, tabs):
            with tab:
                for field in part['fields']:
                    display_field(field)
    else:
        # Display fields directly if no parts are defined
        for field in st.session_state.data_dict:
            display_field(field)


def display_field(field):
    """Helper function to create the correct input based on field 'nature'."""
    if field['nature'] == 'radio':
        value = st.radio(field['label'], field['options'], key=field['key'])
        field['value'] = value
    elif field['nature'] == 'selectbox':
        value = st.selectbox(field['label'], field['options'], key=field['key'])
        field['value'] = value
    elif field['nature'] == 'multiselect':
        value = st.multiselect(field['label'], field['options'], key=field['key'])
        field['value'] = value
    elif field['nature'] == 'date':
        value = st.date_input(field['label'], key=field['key'])
        field['value'] = value
    elif field['nature'] == 'numeric':
        value = st.number_input(field['label'], key=field['key'])
        field['value'] = value
    elif field['nature'] == 'text_area':
        value = st.text_area(field['label'], value=field['value'] if field['value'] else "", key=field['key'])
        field['value'] = value
    else:
        value = st.text_input(label=field['label'], value=field['value'] if field['value'] else "")
        field['value'] = value

page()