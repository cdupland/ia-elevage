import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from model import selector
from util import getYamlConfig
from st_copy_to_clipboard import st_copy_to_clipboard

def display_messages():

    for i, message in enumerate(st.session_state.chat_history):
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                # Display the model from the kwargs
                model = message.kwargs.get("model", "Unknown Model")  # Get the model, default to "Unknown Model"
                st.write(f"**Model :** {model}")
                st.markdown(message.content)
                st_copy_to_clipboard(message.content,key=f"message_{i}")
        
        elif isinstance(message, HumanMessage):
            with st.chat_message("Moi"):
                st.write(message.content)


def launchQuery(query: str = None):

    # Initialize the assistant's response
    full_response = st.write_stream(
        st.session_state["assistant"].ask(
            query,
            prompt_system=st.session_state.prompt_system,
            messages=st.session_state["chat_history"] if "chat_history" in st.session_state else [],
            variables=st.session_state["data_dict"]
        ))

    # Temporary placeholder AI message in chat history
    st.session_state["chat_history"].append(AIMessage(content=full_response, kwargs={"model": st.session_state["assistant"].getReadableModel()}))
    st.rerun()


def show_prompts():
    yaml_data = getYamlConfig()["prompts"]
    
    expander = st.expander("Prompts pré-définis")
    
    for categroy in yaml_data:
        expander.write(categroy.capitalize())

        for item in yaml_data[categroy]:
            if expander.button(item, key=f"button_{item}"):
                launchQuery(item)


def page():
    st.subheader("Posez vos questions")

    if "assistant" not in st.session_state:
        st.text("Assistant non initialisé")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.markdown("<style>iframe{height:50px;}</style>", unsafe_allow_html=True)

    # Collpase for default prompts
    show_prompts()

    # Models selector
    selector.ModelSelector()

    # Displaying messages
    display_messages()


    user_query = st.chat_input("")
    if user_query is not None and user_query != "":

        st.session_state["chat_history"].append(HumanMessage(content=user_query))
        
        # Stream and display response
        launchQuery(user_query)


page()