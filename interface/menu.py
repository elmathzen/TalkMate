import streamlit as st
import base64
import os
import platform
from PIL import Image
from io import BytesIO

from functions.get_language import define_lang
from functions.speech_to_text.micro import select_microphone
from functions.voice.voice_system import NarratorVoice


favicon = Image.open('interface/ressources/favicon_example.png')
st.set_page_config(
    page_title = "Entreprise Assistant",
    page_icon = favicon,
)

# Create three columns with different proportions
col1, col2, col3 = st.columns([2,50,2])


lang = define_lang()
select_microphone(lang)
voice_index = NarratorVoice()
voice_index.select_voice(lang)

# Instantiate voice_id and device_index sessions in the app
voice_id = st.session_state['selected_voice_id']
micro_index = st.session_state['selected_device_index']

# Change the text according to the chosen language
if lang == 'Fr':
    st.sidebar.success("Sélectionnez un micro et une voix")
elif lang == 'En':
    st.sidebar.success("Select a microphone and a voice")

st.sidebar.markdown("---")

if lang == 'Fr':
    st.sidebar.error("Pour développeur uniquement :")
elif lang == 'En':
    st.sidebar.error("For developers only :")

# Add a button to the sidebar that redirects to modelfile.py
if st.sidebar.button('Paramètres Modèles' if lang == 'Fr' else 'Models Parameters'):
    if platform.system() == "Windows":
        os.system("start cmd /K python interface/functions/params_models/modelfile.py")
    else:
        os.system("gnome-terminal -e 'bash -c \"python interface/functions/params_models/modelfile.py; exec bash\"'")

# Add a button to the sidebar that redirects to quantize_model.py
if st.sidebar.button('Quantize Modèles' if lang == 'Fr' else 'Models Quantize'):
    if platform.system() == "Windows":
        os.system("start cmd /K python interface/functions/params_models/quantize_model.py")
    else:
        os.system("gnome-terminal -e 'bash -c \"python interface/functions/params_models/quantize_model.py; exec bash\"'")

# Add a button to the sidebar that redirects to push_to_ollama.py
if st.sidebar.button('Publier Modèles' if lang == 'Fr' else 'Push Models'):
    if platform.system() == "Windows":
        os.system("start cmd /K python interface/functions/params_models/push_to_ollama.py")
    else:
        os.system("gnome-terminal -e 'bash -c \"python interface/functions/params_models/push_to_ollama.py; exec bash\"'")

# Use the middle column for your elements
with col2:
    # Company title
    if lang == 'Fr':
        st.markdown("<h1 style='text-align: center;'>Nom de l'entreprise</h1>", unsafe_allow_html=True)
    elif lang == 'En':
        st.markdown("<h1 style='text-align: center;'>Company Name</h1>", unsafe_allow_html=True)

    # Open image
    logo_entreprise = Image.open('interface/ressources/logo_example.png')

    # Convert image to base64 to display in markdown
    buffered = BytesIO()
    logo_entreprise.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Show image centered
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_str}' width='250'/></div>", unsafe_allow_html=True)

    # Add an H2 title
    if lang == 'Fr':
        st.markdown("<h2 style='text-align: center;'>Bienvenue sur votre Assistant</h2>", unsafe_allow_html=True)
    elif lang == 'En':
        st.markdown("<h2 style='text-align: center;'>Welcome to your Assistant</h2>", unsafe_allow_html=True)

    # Presentation Text
    if lang == 'Fr':
        st.markdown("<p style='text-align: center;'> \
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. \
                    Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. \
                    </p>", 
                    unsafe_allow_html=True)
    elif lang == 'En':
        st.markdown("<p style='text-align: center;'> \
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. \
                    Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. \
                    </p>", 
                    unsafe_allow_html=True)
