import streamlit as st
from datetime import datetime
from util import getYamlConfig

def update_session_state(key,):
    # Get new value from session state and change key for save it in params
    new_value = st.session_state[key]
    key = key[5:]
    
    for item in st.session_state.data_dict:
        if item['key'] == key:
            item['value'] = new_value
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
                    for field_session in st.session_state.data_dict:
                        if field['key'] == field_session['key']:
                            display_field(field_session)

                if st.button(f"Réinitialiser {part['name']}"):
                    resetForm(part['name'])
    else:
        # Display fields directly if no parts are defined
        for field in st.session_state.data_dict:
            display_field(field)
    

    if st.button("Réinitialisation complète"):
        resetForm()

def check_field_condition(field):
    condition = field.get('condition', None)

    if condition is None:
        return True
    
    if condition.get('type') == 'session':
        return st.session_state[condition.get('key')] == condition.get('value')
    

    return False

def display_field(field):
    """Helper function to create the correct input based on field 'nature'."""

    if(check_field_condition(field) == False):
        return

    key = 'form_' + field['key']
    if field['nature'] == 'radio':
        st.radio(
            field['label'],
            field['options'],
            index=field['options'].index(field.get('value')) if field.get('value') in field['options'] else 0,
            key=key,
            on_change=update_session_state,
            args=(key,)
        )

    elif field['nature'] == 'selectbox':
        st.selectbox(
            field['label'], 
            field['options'], 
            index=field['options'].index(field.get('value')) if field.get('value') in field['options'] else 0, 
            key=key, 
            on_change=update_session_state,
            args=(key,)
        )

    elif field['nature'] == 'multiselect':
        st.multiselect(
            field['label'], 
            field['options'], 
            default=[field['options'].index(value) for value in field.get('value') if value in field['options']], 
            key=key, 
            on_change=update_session_state,
            args=(key,)
        )
    elif field['nature'] == 'date':
        date_str = field.get('value', None)
        # Conversion de la chaîne en date, si nécessaire
        if isinstance(date_str, str):
            date_value = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            date_value = date_str
            
        st.date_input(
            field['label'], 
            value=date_value,
            key=key, 
            on_change=update_session_state,
            args=(key,)
        )

    elif field['nature'] == 'numeric':
        st.number_input(field['label'], 
            value=field.get('value', 0), 
            key=key, 
            on_change=update_session_state,
            args=(key,)
        )

    elif field['nature'] == 'text_area':
        st.text_area(field['label'], 
            value=field.get('value', ""), 
            key=key, 
            on_change=update_session_state,
            args=(key,)
        )

    else:
        st.text_input(label=field['label'], 
            value=field.get('value', ""), 
            key=key, 
            on_change=update_session_state,
            args=(key,)
        )

def resetForm(section: str = None):
    
    for field in st.session_state.data_dict:
        if section is None or section == field['part']:
            field['value'] = None

    st.rerun()


page()