import streamlit as st
import os
import json
import uuid
import tempfile

from functions.get_language import get_lang
from functions.interface_fct.page_title import set_page_title
from functions.get_model import get_model_names
from functions.interface_fct.qa_document.qa_text_mode import query_qa_document
from functions.interface_fct.qa_document.qa_discussion import discussion_qa_document


user_doc = None
user_id = ""
session_name = 'qa_document'
history_dir = "conversation_qa_document"
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

# Initialize session_name with an empty list for messages
if session_name not in st.session_state:
    st.session_state[session_name] = []

session_state_updated = st.session_state[session_name]

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

# Add a picker to choose a chat history file
history_files = os.listdir(history_dir)
selected_file = st.sidebar.selectbox("Historique de conversation" if lang == 'Fr' else 
                                    "Conversation history file", [""] + history_files)

# Upload a file
st.title("Upload de fichier" if lang == 'Fr' else "Upload file")
uploaded_file = st.file_uploader("Choisissez un fichier" if lang == 'Fr' else "Choose a file", type=['pdf', 'txt', 'csv'])

# If user upload a file
if uploaded_file is not None:
    # Create the 'chroma' and 'temp_file' folders if they don't exist
    if not os.path.exists('temp_chroma/temp_file'):
        os.makedirs('temp_chroma/temp_file')

    # Get the extension of the uploaded file
    extension = os.path.splitext(uploaded_file.name)[1]

    # Create a temporary file in the 'chroma/temp_file' folder with the same extension as the uploaded file
    with tempfile.NamedTemporaryFile(suffix=extension, dir='temp_chroma/temp_file', delete=False) as tmp:
        tmp.write(uploaded_file.read())
        user_doc = tmp.name  # Get the path of the temporary file

    # Generate a unique user_id each time a user uploads a file
    user_id = str(uuid.uuid4())

try:
    micro_device = st.session_state['selected_device_index']
except KeyError:
    st.sidebar.warning("Veuillez aller dans le menu pour définir votre micro et la voix synthétique." if lang == "Fr" else
                       "Please go to the menu to set your microphone and the synthetic voice.")
    micro_device = None

# Use text chat and text function if user upload a file
if user_doc is not None:
    query = st.chat_input("Posez une question sur votre document" if lang == 'Fr' else "Ask a Question on your document")
    query_qa_document(user_doc, query, user_id, llm_model, embeddings_model, lang, session_state_updated, selected_file, history_dir, session_name)

# If user click on discussion button, active the discussion function
if micro_device is not None:
    discussion_qa_document(lang, user_doc, user_id, llm_model, embeddings_model, micro_device, session_state_updated, selected_file, history_dir, session_name)

# Recover json load file if the user select and load a json
if selected_file:
    with open(os.path.join(history_dir, selected_file), "r", encoding="utf8") as f:
        st.session_state[session_name] = json.load(f)

# Show all previous posts
for message in st.session_state[session_name]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Use the function to set the page title
set_page_title("QA Document · Streamlit", "❓QA sur un Document" if lang == "Fr" else "❓QA Document")