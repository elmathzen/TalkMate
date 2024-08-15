import streamlit as st 
from functions.RAG_System.rag import CustomProcessor
from functions.interface_fct.rag_page.rag_save_history import rag_create_save_history


class RAG_Text():
    def __init__(self, lang, llm_model, embeddings_model, question, actual_profile, history_dir, session_name):
        self.lang = lang
        self.llm_model = llm_model
        self.embeddings_model = embeddings_model
        self.question = question
        self.actual_profile = actual_profile
        self.history_dir = history_dir
        self.session_name = session_name

    def rag_text_files_load(self, urls, uploaded_files):
        rag = CustomProcessor(language=self.lang, llm_model=self.llm_model, embeddings_model=self.embeddings_model, actual_profile=self.actual_profile)
        resources = urls + [file.getvalue() for file in uploaded_files]
        doc_splits = rag.process_ressources(resources)
        rag.process_vectorization(doc_splits)
        st.success("Vectorisation effectuée avec succès !" if self.lang == 'Fr' else "Vectorization done successfully !")

    def rag_text_prompt(self):
        rag = CustomProcessor(language=self.lang, llm_model=self.llm_model, embeddings_model=self.embeddings_model, actual_profile=self.actual_profile)

        # Check if the profile has changed
        if 'previous_profile' in st.session_state and st.session_state['previous_profile'] != self.actual_profile:
            st.session_state[self.session_name] = []
            
        # Update the previous profile
        st.session_state['previous_profile'] = self.actual_profile

        # When user put his question start the RAG
        if self.question:
            with st.spinner('Processing...'):
                # Retrieve the vectorized documents
                retriever = rag.load_vectorized_documents()
                response = rag.process_response(retriever, self.question)
                
                # Add the question and response to the conversation
                st.session_state[self.session_name].append({"user": self.question, "assistant": response})

                # Display the conversation
                for i in range(len(st.session_state[self.session_name])):
                    st.write(f"❓User: {st.session_state[self.session_name][i]['user']}")
                    st.write(f"🤖Assistant: {st.session_state[self.session_name][i]['assistant']}")

                rag_create_save_history(self.history_dir, self.actual_profile, self.session_name)