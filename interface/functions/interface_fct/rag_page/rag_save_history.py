import os
import json
import re
import nltk
import streamlit as st
from nltk.corpus import stopwords


def rag_create_save_history(history_dir, actual_profile, session_name):
    # Download stopwords if they are not already downloaded
    try:
        nltk.corpus.stopwords.words('english')
        nltk.corpus.stopwords.words('french')
    except LookupError:
        nltk.download('stopwords')

    # Check if the history directory exists, if not create it
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    # Create file name from user's words and clean the text
    stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))
    first_user_message = st.session_state[session_name][0]['user']
    cleaned_message = re.sub(r'\W+', ' ', first_user_message).lower()
    cleaned_message = " ".join(word for word in cleaned_message.split() if word not in stop_words)
    history_file_name = "[" + actual_profile + "]" + " " + " ".join(cleaned_message.split()[:5]) + ".json"

    # Save the conversation to a JSON file
    with open(os.path.join(history_dir, history_file_name), 'w', encoding="utf8") as f:
        json.dump(st.session_state[session_name], f, indent=4, ensure_ascii=False)