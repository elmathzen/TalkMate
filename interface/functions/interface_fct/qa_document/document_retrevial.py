import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community import embeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA


def document_qa(user_doc, query, user_id, model_llm="mistral", model_embeddings="nomic-embed-text"):
    # Create a unique folder for each user
    folder_name = f'temp_chroma/user_{user_id}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Choose the appropriate loader based on the file extension
    extension = os.path.splitext(user_doc)[1]
    if extension == '.pdf':
        loader = PyPDFLoader(user_doc)
    elif extension == '.txt':
        loader = TextLoader(user_doc)
    elif extension == '.csv':
        loader = CSVLoader(user_doc)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    document = loader.load()

    # Split documents
    text_splitter = CharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    texts = text_splitter.split_documents(document)

    # Use chromadb to build temp vector database locally on the user's computer
    doc_search = Chroma.from_documents(
        documents=texts, 
        collection_name=f'user_{user_id}',
        embedding=embeddings.OllamaEmbeddings(model=model_embeddings),
        persist_directory=folder_name,
    )

    llm = Ollama(model=model_llm)

    # Use RetrievalQA to query on a document
    retriever = doc_search.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    result = chain.run(query)
    
    return result