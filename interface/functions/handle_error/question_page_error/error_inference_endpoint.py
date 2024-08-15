import platform
import subprocess
import streamlit as st


def handle_error_inference_endpoint(lang):
    if lang == "Fr":
        print("Erreur détectée, résolution en cours...")
    else: 
        print("Error detected, resolving in progress...")
    
    if platform.system() == "Windows":
        subprocess.Popen(["start", "/min", "cmd", "/k", "ollama serve"], shell=True)
        st.sidebar.info("Erreur résolue ! Désolé pour la gêne occasionnée" if lang == "Fr" else 
                        "Error resolved! Sorry for the inconvenience")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        subprocess.Popen(["gnome-terminal", "--", "ollama serve"])
        st.sidebar.info("Erreur résolue ! Désolé pour la gêne occasionnée" if lang == "Fr" else 
                        "Error resolved! Sorry for the inconvenience")
    else:
        print("OS non supporté lancez 'ollama serve' dans un nouveau terminal" if lang == "Fr" else 
              "OS not supported, run 'ollama serve' in a new shell")