import streamlit as st
import json 
import os
import unicodedata
import re

from functions.get_language import get_lang
from functions.interface_fct.page_title import set_page_title
from functions.RAG_System.rag import CustomProcessor
from functions.interface_fct.rag_page.rag_app_button import RAGButton
from functions.interface_fct.rag_page.rag_text_mode import RAG_Text
from functions.interface_fct.rag_page.rag_discussion_mode import RAG_Discussion
from functions.get_model import get_model_names

from functions.handle_error.question_page_error.error_inference_endpoint import handle_error_inference_endpoint


session_name = 'conversation'
history_dir = 'conversation_rag'
load_vectorize = None
try:
    # Initialize the conversation in the session state if it doesn't exist
    if session_name not in st.session_state:
        st.session_state[session_name] = []

    lang = get_lang()
    model_names = get_model_names()
    model_names.insert(0, "")
    llm_model = st.sidebar.selectbox("🔬 Modèles" if lang == "Fr" else '🔬 Models', model_names)
    if not llm_model:
        st.sidebar.warning("Veuillez choisir un modèle" if lang == 'Fr' else "Please choose a model")

    model_embed_names = get_model_names()
    model_embed_names.insert(0, "")
    embeddings_model = st.sidebar.selectbox("Modèles Embeddings" if lang == "Fr" else "Embeddings Models", model_embed_names)
    if not embeddings_model:
        st.sidebar.warning("Veuillez choisir un modèle d'embedding" if lang == 'Fr' else "Please choose an embedding model")

    st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    # Retrieve all folders (profils) in 'interface/functions/RAG_System'
    base_dir = 'interface/functions/RAG_System'
    profiles = [name for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name)) 
                and name not in ['__pycache__', 'temp-file']]
    profiles.insert(0, '')

    # Add 'default_profil' to the list of profiles if it does not already exist
    if 'default_profil' not in profiles:
        profiles.insert(1, 'default_profil')

    # Profile Selector
    actual_profile = st.sidebar.selectbox("Sélectionnez un profil" if lang == 'Fr' else "Select a profil", profiles)
    if actual_profile == '':
        # Input for the name of a new profil if the user want
        new_profile_name = st.sidebar.text_input("Entrez le nom du nouveau profil" if lang == 'Fr' else "Enter the name of the new profile")
        if not new_profile_name == '':
            # Remove accents
            new_profile_name = unicodedata.normalize('NFD', new_profile_name).encode('ascii', 'ignore').decode("utf-8")
            # Remove punctuations except underscore
            new_profile_name = re.sub(r'[^\w\s]', '', new_profile_name)
            # Replace spaces with underscores
            new_profile_name = new_profile_name.replace(' ', '_')
            # Button to create the new profile
            if st.sidebar.button("Créer" if lang == 'Fr' else "Create"):
                new_profile_path = os.path.join(base_dir, new_profile_name)
                if not os.path.exists(new_profile_path):
                    os.makedirs(new_profile_path)
                    st.rerun()
                else:
                    st.sidebar.error(f"Le profil {new_profile_name} existe déjà." if lang == 'Fr' else f"The {new_profile_name} profile already exists.")

    if not actual_profile == '':
        # Button to delete current profile
        if st.sidebar.button("Supprimer profil actuel" if lang == 'Fr' else "Delete actual profil"):
            try:
                rag = CustomProcessor(language=lang, llm_model=llm_model, embeddings_model=embeddings_model, actual_profile=actual_profile)
                rag.delete_profile()
                st.rerun()
            except Exception as e:
                st.error("Veuillez redémarrer l\'application pour supprimer correctement le profil." if lang == 'Fr' else 
                         "Please restart the application to delete the profile correctly.")
            
        st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)
            
        load_vectorize = st.sidebar.checkbox("Base de donnée actuelle" if lang == 'Fr' else "Current Database")

    st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    # Add a picker to choose a chat history file
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    history_files = os.listdir(history_dir)
    selected_file = st.sidebar.selectbox("Historique des conversations" if lang == 'Fr' else 
                                         "Conversation history files", [""] + history_files)
    
    # Load the selected conversation
    if selected_file:
        st.session_state[session_name] = []
        with open(f'{history_dir}/{selected_file}', 'r', encoding="utf8") as f:
            loaded_conversation = json.load(f)
            # Display the loaded conversation
            for i in range(len(loaded_conversation)):
                st.write(f"❓User: {loaded_conversation[i]['user']}")
                st.write(f"🤖Assistant: {loaded_conversation[i]['assistant']}")

        rag_app_btn = RAGButton(lang, history_dir, selected_file)
        rag_app_btn.rename_file()
        rag_app_btn.download_as_csv()
        rag_app_btn.delete_file(selected_file)
    
    if not selected_file:
        # Set messages in different languages
        messages = {
            "Fr": {
                "title": "Assistant sur vos Données",
                "url_text": "Entrez les URL ici (une par ligne):",
                "file_uploader_text": "Choisissez vos fichiers à traiter",
            },
            "En": {
                "title": "Assistant to your Data",
                "url_text": "Enter the URL here (one per line):",
                "file_uploader_text": "Choose your files to process",
            }
        }

        # Use messages according to the chosen language
        lang_messages = messages.get(lang, messages["En"])

        question = None

        if load_vectorize == False:
            # Show UI elements with corresponding messages
            st.title(lang_messages["title"])
            urls = st.text_area(lang_messages["url_text"])
            urls = urls.split("\n")

            uploaded_files = st.file_uploader(lang_messages["file_uploader_text"], type=["pdf"], accept_multiple_files=True)
            if not uploaded_files and not urls[0]:
                st.warning("Veuillez rentrer au moins une ressource à traiter" if lang == 'Fr' else 
                           "Please enter at least one resource to process")
            else:
                if llm_model and embeddings_model:
                    if st.button("Vectoriser" if lang == 'Fr' else "Vectorize"):
                        # RAG Text add Documents
                        rag_text = RAG_Text(lang, llm_model, embeddings_model, question, actual_profile, history_dir, session_name)
                        rag_text.rag_text_files_load(urls, uploaded_files)

        elif load_vectorize == True: 
            question = st.chat_input("Entrez votre question ici :" if lang == 'Fr' else "Enter your question here :")
            if question == None: 
                st.sidebar.warning("Veuillez saisir une question" if lang == "Fr" else "Please enter a question")
            else: 
                # RAG Text
                rag_text = RAG_Text(lang, llm_model, embeddings_model, question, actual_profile, history_dir, session_name)
                rag_text.rag_text_prompt()

            try:
                micro_device = st.session_state['selected_device_index']
            except KeyError:
                st.sidebar.warning("Veuillez aller dans le menu pour définir votre micro et la voix synthétique." if lang == "Fr" else
                                "Please go to the menu to set your microphone and the synthetic voice.")
                micro_device = None

            if micro_device is not None:
                # RAG Discussion
                rag_discussion = RAG_Discussion(lang, llm_model, embeddings_model, question, micro_device, actual_profile, history_dir, session_name)
                rag_discussion.rag_discussion_prompt()

        else:
            st.warning("Veuillez choisir ou créer un profile" if lang == 'Fr' else "Please choose or create a profile")

        st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

except ValueError as e:
    if "Error raised by inference endpoint" in str(e):
        handle_error_inference_endpoint(lang)

# Use the function to set the page title
set_page_title("Question · Streamlit", "🛠️ Question")