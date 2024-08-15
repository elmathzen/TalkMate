import streamlit as st
from functions.interface_fct.save_history import create_and_save_history
from functions.interface_fct.qa_document.document_retrevial import document_qa
from functions.speech_to_text.record import record_audio
from functions.speech_to_text.speech import SpeechToText
from functions.voice.voice_system import NarratorVoice


def discussion_qa_document(lang, user_doc, user_id, model_llm, model_embeddings, micro_index, session_state_updated, selected_file, history_dir, session_name):
    if st.sidebar.button('🎙️ Mode Discussion' if lang == 'Fr' else '🎙️ Discussion Mode'):
        if lang == "Fr":
            st.sidebar.info("Écoute..")
        else: 
            st.sidebar.info("Listen..")

        # Recording audio
        record_audio(filename="interface/functions/speech_to_text/temp_audio/audio.wav", device_index=micro_index, rate=44100, chunk=1024, threshold=200, pre_recording_buffer_length=2)

        if lang == "Fr":
            st.sidebar.warning("Transcription en cours..")
        else: 
            st.sidebar.warning("Transcription in progress..")

        # Transcription Speech To Text
        speech = SpeechToText()
        query = speech.transcribe("interface/functions/speech_to_text/temp_audio/audio.wav")
        
        if lang == "Fr":
            st.sidebar.success("Transcription terminée")
        else: 
            st.sidebar.success("Transcription completed")

        # Add the input message to the message history
        session_state_updated.append({'role': 'user', 'content': query})

        result = document_qa(user_doc, query, user_id, model_llm, model_embeddings)

        # Add the Exit Message to the Message History
        session_state_updated.append({'role': 'assistant', 'content': result})

        # Show all previous posts
        for message in st.session_state[session_name]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Use synthetic voice
        voice = NarratorVoice()
        voice.speak(result)

        # Save in new json file if first prompt or an already existing json and add updated prompt
        selected_file = create_and_save_history(session_state_updated, selected_file, history_dir, session_name)

    return session_state_updated