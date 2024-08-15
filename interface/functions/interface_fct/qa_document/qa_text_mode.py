import streamlit as st
from functions.interface_fct.app_button import AppButton
from functions.interface_fct.save_history import create_and_save_history
from functions.interface_fct.qa_document.document_retrevial import document_qa


def query_qa_document(user_doc, query, user_id, model_llm, model_embeddings, lang, session_state_updated, selected_file, history_dir, session_name):
    # Button to rename, download and delete .json files
    app_btn = AppButton(lang, history_dir, selected_file, session_name)

    # Recover json load file if the user select and load a json
    if selected_file:
        app_btn.rename_file()
        app_btn.download_as_csv()
        app_btn.delete_file()

    if not selected_file:
        app_btn.new_file()

    if query:
        # Add the input message to the message history
        session_state_updated.append({'role': 'user', 'content': query})

        result = document_qa(user_doc, query, user_id, model_llm, model_embeddings)

        # Add the Exit Message to the Message History
        session_state_updated.append({'role': 'assistant', 'content': result})

        # Show all previous posts
        for message in st.session_state[session_name]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Save in new json file if first prompt or an already existing json and add updated prompt
        selected_file = create_and_save_history(session_state_updated, selected_file, history_dir, session_name)

    return session_state_updated