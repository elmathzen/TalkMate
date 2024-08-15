import streamlit as st 
import json 
import os
from functions.interface_fct.assistant_page.process_discussion import process_discussion


def discussion_prompt(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name):  
    # Recover json load file if the user select and load a json
    if selected_file:
        with open(os.path.join(history_dir, selected_file), "r", encoding="utf8") as f:
            st.session_state[session_name] = json.load(f)

    continue_discussion = st.session_state['continue_discussion']
    if continue_discussion == False:
        if st.sidebar.button('🎙️ Mode Discussion' if lang == 'Fr' else '🎙️ Discussion Mode'):
            return process_discussion(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name)
    else: 
        stop_button = st.sidebar.button('Stop')
        while not stop_button:
            session_state_updated = process_discussion(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name)
            # Update the stop button status at the end of each loop
            stop_button = st.sidebar.button('Stop')

        return session_state_updated