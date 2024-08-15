import streamlit as st
import pandas as pd
import io
import docx2txt
from PyPDF2 import PdfReader


def extract_text_from_file(uploaded_file, lang):
    if uploaded_file is not None:
        # Read file contents based on its type
        if uploaded_file.type == 'text/plain':
            # Extract text from .txt file
            text = io.TextIOWrapper(uploaded_file, encoding='utf-8').read()
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            # Extract text from .docx file
            text = docx2txt.process(uploaded_file)
        elif uploaded_file.type == 'application/pdf':
            # Extract text from .pdf file
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif uploaded_file.type == 'text/csv':
            # Extract text from .csv file
            df = pd.read_csv(uploaded_file)
            text = df.to_string(index=False)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            # Extract text from .xlsx file
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            text = df.to_string(index=False)
        else:
            st.write("Type de fichier non pris en charge" if lang == "Fr" else "Unsupported file type")
            return None
        
        # Replace line breaks with spaces
        text = text.replace('\n', ' ')
        
        return text