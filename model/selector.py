import streamlit as st
from .ModelIntegrations import ModelManager
    
def ModelSelector():
    # Dictionnaire des modèles par fournisseur
    model_providers = {
        "Mistral": {
            "mistral-large-latest": "mistral.mistral-large-latest",
            "open-mixtral-8x7b": "mistral.open-mixtral-8x7b",
        },
        "OpenAI": {
            "gpt-4o": "openai.gpt-4o",
        },
        "Anthropic": {
            "claude-3-5-sonnet-20240620": "anthropic.claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229": "anthropic.claude-3-opus-20240229",
            "claude-3-sonnet-20240229": "anthropic.claude-3-sonnet-20240229",
        },
        # "llama": {
        #     "llama3.2-11b-vision": "llama.llama3.2-11b-vision",
        #     "llama3.2-1b": "llama.llama3.2-1b",
        #     "llama3.2-3b": "llama.llama3.2-3b"
        # }
    }

    # Créer une liste avec les noms de modèle, groupés par fournisseur (fournisseur - modèle)
    model_options = []
    model_mapping = {}

    for provider, models in model_providers.items():
        for model_name, model_instance in models.items():
            option_name = f"{provider} - {model_name}"
            model_options.append(option_name)
            model_mapping[option_name] = model_instance

    # Sélection d'un modèle via un seul sélecteur
    selected_model_option = st.selectbox("Choisissez votre modèle", options=model_options)

    if(st.session_state["assistant"]):
        splitter = model_mapping[selected_model_option].split(".")
        st.session_state["assistant"].setModel(ModelManager().get_model(splitter[0], splitter[1]), splitter[1])
    