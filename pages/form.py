# python
import streamlit as st
from util import getYamlConfig

def update_session_state(key):
    for item in st.session_state.data_dict:
        if item['key'] == key:
            item['value'] = st.session_state[key]
            break

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
        # Display fields directly si aucune partie définie
        for field in st.session_state.data_dict:
            display_field(field)

def display_field(field):
    """Helper function to create the correct input based on field 'nature'."""
    key = field['key']
    if field['nature'] == 'radio':
        st.radio(field['label'], field['options'], key=key, on_change=update_session_state, args=(key,))
    elif field['nature'] == 'selectbox':
        st.selectbox(field['label'], field['options'], key=key, on_change=update_session_state, args=(key,))
    elif field['nature'] == 'multiselect':
        st.multiselect(field['label'], field['options'], key=key, on_change=update_session_state, args=(key,))
    elif field['nature'] == 'date':
        st.date_input(field['label'], key=key, on_change=update_session_state, args=(key,))
    elif field['nature'] == 'numeric':
        st.number_input(field['label'], value=field.get('value', 0), key=key, on_change=update_session_state, args=(key,))
    elif field['nature'] == 'text_area':
        st.text_area(field['label'], value=field.get('value', ""), key=key, on_change=update_session_state, args=(key,))
    else:
        st.text_input(label=field['label'], value=field.get('value', ""), key=key, on_change=update_session_state, args=(key,))

page()