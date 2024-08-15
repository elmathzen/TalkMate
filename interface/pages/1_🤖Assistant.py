import streamlit as st
import os

from functions.get_model import get_model_names
from functions.get_language import get_lang
from functions.interface_fct.page_title import set_page_title
from functions.interface_fct.assistant_page.text_mode import text_prompt
from functions.interface_fct.assistant_page.discussion_mode import discussion_prompt


session_name = 'session_state'
history_dir = "conversation_history"
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

# Initialize 'session_state' with an empty list for messages
if session_name not in st.session_state:
    st.session_state[session_name] = []

session_state_updated = st.session_state[session_name]

lang = get_lang()
model_names = get_model_names()
model_names.insert(0, "")
model_use = st.sidebar.selectbox('🔬 Modèles' if lang == "Fr" else '🔬 Models', model_names)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Add a picker to choose a chat history file
history_files = os.listdir(history_dir)
selected_file = st.sidebar.selectbox("Historique de conversation" if lang == 'Fr' else 
                                    "Conversation history file", [""] + history_files)

try:
    micro_device = st.session_state['selected_device_index']
except KeyError:
    st.sidebar.warning("Veuillez aller dans le menu pour définir votre micro et la voix synthétique." if lang == "Fr" else
                    "Please go to the menu to set your microphone and the synthetic voice.")
    micro_device = None

prompt = st.chat_input("Posez une question" if lang == 'Fr' else "Ask a Question")

text_prompt(prompt, lang, model_use, session_state_updated, selected_file, history_dir, session_name)

if micro_device is not None:
    st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    # Change the parameter if the user want a continue discussion or not
    st.session_state['continue_discussion'] = False
    st.session_state['continue_discussion'] = st.sidebar.checkbox('Discussion continue' if lang == 'Fr' else 
                                                                  'Continue Discussion', value=st.session_state['continue_discussion'])
    
    discussion_prompt(lang, model_use, micro_device, session_state_updated, selected_file, history_dir, session_name)

# Show all previous posts
for message in st.session_state[session_name]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Use the function to set the page title
set_page_title("Assistant · Streamlit", "🤖 Assistant")