import streamlit as st 
import ollama
from functions.interface_fct.save_history import create_and_save_history
from functions.speech_to_text.record import record_audio
from functions.speech_to_text.speech import SpeechToText
from functions.voice.voice_system import NarratorVoice


def process_discussion(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name):
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
    text = speech.transcribe("interface/functions/speech_to_text/temp_audio/audio.wav")

    # Add user prompt to session updated
    session_state_updated.append({
        "role": "user",
        "content": text,
    })

    if lang == "Fr":
        st.sidebar.success("Transcription terminée")
    else: 
        st.sidebar.success("Transcription completed")

    # Push the user prompt in the LLM model and return response
    with st.spinner("Réflexion.." if lang == 'Fr' else "Thinking.."):
        result = ollama.chat(model=model_use, messages=session_state_updated)
        response = result["message"]["content"]

        # Add model response to message list
        session_state_updated.append({
            "role": "assistant",
            "content": response,
        })

    if lang == "Fr":
        st.sidebar.success("Réponse de l'assistant obtenue")
    else: 
        st.sidebar.success("Assistant response received")

    # Show all previous posts
    for message in st.session_state[session_name]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Use NarratorVoice to speak the response
    narrator = NarratorVoice()
    narrator.speak(response)

    # Save in new json file if first prompt or an already existing json and add updated prompt
    selected_file = create_and_save_history(session_state_updated, selected_file, history_dir, session_name)

    return session_state_updated