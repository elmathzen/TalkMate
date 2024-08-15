import os
import subprocess
import webbrowser
from colors import *


def push_ollama_interface():
    # Ask the user which language they want to use
    language = input(f"{CYAN}Type 1 for English, 2 for French: {RESET}")
    while language not in ['1', '2']:
        language = input(f"{RED}Entrée non valide. Veuillez taper 1 pour l'anglais, 2 pour le français : {RESET}")

    language = int(language)
    
    # Get the full path to the SSH public key
    ssh_pub_key_path = os.path.expanduser('~/.ollama/id_ed25519.pub')

    command = f'{ssh_pub_key_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    # Open the Ollama website
    webbrowser.open('https://ollama.com/')

    if language == 2:
        print(f"{GREEN}\nVeuillez vous connecter à votre compte sur la plateforme Ollama et placer votre clé SSH dans vos paramètres de compte.\n{RESET}")
    else: 
        print(f"{GREEN}\nPlease log in to your account on the Ollama platform and place your SSH key in your account settings.\n{RESET}")

    # Try to serve with Ollama
    try:
        os.system('ollama serve 2> /dev/null')
    except Exception:
        pass

    while True:
        print(f"{CYAN}\nExemple{RESET}" if language == 2 else f"{CYAN}\nExample{RESET}")
        print(f"{CYAN}ton_modèle:Q4_0\n{RESET}" if language == 2 else f"{CYAN}your_model:Q4_0\n{RESET}")

        # List with Ollama
        os.system('ollama list')

        # Ask the user for their account name and model
        if language == 2:
            account_name = input(f"{CYAN}\nVeuillez entrer le nom de votre compte : \n{RESET}")
            model_name = input(f"{CYAN}\nQuel modèle voulez-vous pousser sur Ollama ? \n{RESET}")
        else: 
            account_name = input(f"{CYAN}\nPlease enter your account nam : \n{RESET}")
            model_name = input(f"{CYAN}\nWhich model do you want to push to Ollama ? \n{RESET}")

        # Copy and push the model with Ollama
        os.system(f"ollama cp {model_name} {account_name}/{model_name}")
        os.system(f"ollama push {account_name}/{model_name}")

        # Ask the user if they want to push another model
        if language == 2:
            continue_push = input(f"{CYAN}\nVoulez-vous pousser un autre modèle ? Tapez 1 pour oui, tout autre chose pour non : \n{RESET}")
        else:
            continue_push = input(f"{CYAN}\nDo you want to push another model? Type 1 for yes, anything else for no : \n{RESET}")

        # Break the loop if the user does not want to push another model
        if continue_push != '1':
            break


push_ollama_interface()