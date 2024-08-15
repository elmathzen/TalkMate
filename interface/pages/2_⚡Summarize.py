import base64
import streamlit as st
import pandas as pd

from functions.get_language import get_lang
from functions.interface_fct.page_title import set_page_title
from functions.voice.voice_system import NarratorVoice
from functions.interface_fct.summarize_page.file_to_text import extract_text_from_file
from functions.interface_fct.summarize_page.summarize import summarize_model
from functions.interface_fct.summarize_page.display_properties import display_options


lang = get_lang()

# Add a button to toggle the synthetic voice or not
audio_mode = st.sidebar.checkbox("Mode Audio" if lang =="Fr" else "Audio Mode", key="audio_mode")

st.sidebar.markdown("<hr style='margin:2px;'>", unsafe_allow_html=True)

if lang == 'Fr':
    st.title("Résumer un Fichier")
elif lang == 'En':
    st.title("Summary a File")

# Add a button to toggle the visibility of advanced options
advanced_options = st.sidebar.checkbox("Propriétés Avancées" if lang =="Fr" else "Advanced Properties", key="advanced")

# Add sliders for max_length and min_length in the sidebar
if advanced_options:
    max_length, min_length, batch_size, top_k, top_p = display_options(lang)

# Add a file uploader to the sidebar
message_pdf = "Choisissez un fichier PDF" if lang == 'Fr' else "Choose a PDF file"
uploaded_file = st.file_uploader("\n", type=['pdf', 'txt', 'docx', 'csv', 'xlsx'])
summary = None
if uploaded_file is not None:
    st.write('Fichier chargé avec succès !' if lang == 'Fr' else 'File loaded successfully !')
    text = extract_text_from_file(uploaded_file, lang)
    if st.button('Résumer' if lang == "Fr" else "Summarize"):
        if advanced_options:
            summary = summarize_model(text, max_length=max_length, min_length=min_length, batch_size=batch_size, top_k=top_k, top_p=top_p)
        else: 
            summary = summarize_model(text)
        final_summary = st.write(summary)
        if audio_mode:
            # Use NarratorVoice to speak the response
            narrator = NarratorVoice()
            narrator.speak(summary)

    # Show extracted text
    st.text_area("Extrait Texte  :" if lang == "Fr" else "Text Extract", text, height=300, disabled=True)

if summary:
    if lang == "Fr":
        data = {'Texte Original': [text], 'Résumé': [summary]}
    else: 
        data = {'Original Text': [text], 'Summary': [summary]}
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    file_name = 'summary.csv'
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Cliquez pour télécharger</a>' if lang == 'Fr' else \
           f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Click to download</a>'
    st.markdown(href, unsafe_allow_html=True)

# Use the function to set the page title
set_page_title("Summarize · Streamlit", "⚡Résumer" if lang == "Fr" else "⚡Summarize")