import os
import shutil
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter 


class CustomProcessor:
    def __init__(self, language="En", llm_model="mistral", embeddings_model="nomic-embed-text", actual_profile="default_profil"):
        self.language = language
        self.llm_model = llm_model
        self.embeddings_model = embeddings_model
        self.actual_profile = actual_profile

        # Get the current script directory
        script_dir = os.path.dirname(os.path.realpath(__file__))

        self.db_dir = os.path.join(script_dir, self.actual_profile)
        os.makedirs(self.db_dir, exist_ok=True)

        self.temp_dir = os.path.join(script_dir, "temp-file")
        os.makedirs(self.temp_dir, exist_ok=True)

    def process_ressources(self, resources):
        docs = []
        for resource in resources:
            if isinstance(resource, str):
                if resource.startswith("http"):
                    docs.extend(WebBaseLoader(resource).load())
            else:
                temp_file_path = os.path.join(self.temp_dir, "temp.pdf")
                with open(temp_file_path, "wb") as f:
                    f.write(resource)
                    docs.extend(PyPDFLoader(temp_file_path).load())

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
        doc_splits = text_splitter.split_documents(docs)
        return doc_splits
    
    def process_vectorization(self, doc_splits):
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name=self.actual_profile,
            embedding=embeddings.OllamaEmbeddings(model=self.embeddings_model),
            persist_directory=self.db_dir,
        )
        retriever = vectorstore.as_retriever()
        return retriever

    def process_response(self, retriever, question):
        model_local = Ollama(model=self.llm_model)
        if self.language == "Fr":
            after_rag_template = """Répond à la question en français en te basant uniquement sur le contexte suivant:
            Contexte: {context}
            Question: {question}
            """
        else: 
            after_rag_template = """Answer to the question in english based only on the following context:
            Context: {context}
            Question: {question}
            """

        after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
        after_rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | after_rag_prompt
            | model_local
            | StrOutputParser()
        )
        return after_rag_chain.invoke(question)
    
    def load_vectorized_documents(self):        
        # Load the existing vector database
        vectorstore = Chroma(
            collection_name=self.actual_profile,
            embedding_function=embeddings.OllamaEmbeddings(model=self.embeddings_model),
            persist_directory=self.db_dir
        )
        retriever = vectorstore.as_retriever()
        return retriever
    
    def delete_profile(self):
        # Checks if the profile directory exists
        if os.path.exists(self.db_dir):
            # Deletes the directory from the profile
            shutil.rmtree(self.db_dir)