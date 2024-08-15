import os
import re
import glob
import time
import platform
import subprocess
import webbrowser
from transformers import AutoModelForCausalLM, AutoTokenizer
from colors import *


def quantize_model_interface():
    # Ask the user which language they want to use
    language = input(f"{CYAN}Type 1 for English, 2 for French: {RESET}")
    while language not in ['1', '2']:
        language = input(f"{RED}Invalid entry. Please type 1 for English, 2 for French: {RESET}")

    language = int(language)
    while True:
        if language == 2:
            model_name = input(f"{GREEN}\nVeuillez entrer le nom du modèle que vous souhaitez télécharger :\n{RESET}")
        else: 
            model_name = input(f"{GREEN}\nPlease enter the model name you want to download :\n{RESET}")
            
        try:
            print("")
            AutoTokenizer.from_pretrained(model_name)
            AutoModelForCausalLM.from_pretrained(model_name)
            break
        except subprocess.CalledProcessError:
            print(f"{RED}Le nom du modèle n'est pas valide. Veuillez réessayer.{RESET}" if language == 2 else f"{RED}The model name is invalid. Try Again.{RESET}")

    # Check if Docker is installed
    try:
        subprocess.check_output('docker -v', shell=True)
        docker_installed = True
    except subprocess.CalledProcessError:
        docker_installed = False

    while True:
        if docker_installed:
            try:
                subprocess.run(["docker", "run", "-d", "ollama/quantize"], check=True)
                break
            except subprocess.CalledProcessError:
                print(f"{RED}Docker n'est pas lancé. Veuillez ouvrir l'application Docker et appuyez sur 1 puis Entrée pour continuer.{RESET}" if language == 2 else f"{RED}Docker is not running. Please open the Docker application and enter 1 to continue.{RESET}")
        else:
            print(f"{RED}Docker n'est pas installé. Redirection vers la page de téléchargement officielle de Docker...{RESET}" if language == 2 else f"{RED}Docker is not installed. Redirecting to the official Docker download page...{RESET}")
            webbrowser.open('https://www.docker.com/products/docker-desktop')

        input_value = int(input())
        if input_value == 1:
            try:
                subprocess.check_output('docker -v', shell=True)
                docker_installed = True
            except subprocess.CalledProcessError:
                docker_installed = False

    # New code to navigate to the model directory and run the docker command
    model_dir = os.path.join("C:\\Users", os.getlogin(), ".cache", "huggingface", "hub", "models--" + model_name.replace("/", "--"), "snapshots")

    # Check if the directory exists
    if os.path.isdir(model_dir):
        os.chdir(model_dir)

        # Navigate to the only subdirectory in the 'snapshots' directory
        subdirs = glob.glob('./*/') 
        if len(subdirs) == 1:
            os.chdir(subdirs[0])
        else:
            if language == 2:
                print("Erreur : un sous-répertoire attendu dans le répertoire « instantanés »")
            else:
                print("Error: Expected one subdirectory in 'snapshots' directory")
    else:
        if language == 2:
            print(f"Erreur : Le chemin d'accès spécifié est introuvable: {model_dir}")
        else:
            print(f"Error: The specified path could not be found: {model_dir}")

    try:
        subprocess.run(["docker", "run", "--rm", "-v", ".:/model", "ollama/quantize"], check=True)
    except subprocess.CalledProcessError:
        pass
    if language == 2:
        print(f"{GREEN}Voici toutes les quantifications possibles que nous pouvons utiliser{RESET}")
    else: 
        print(f"{GREEN}Here all the possible quantization that we can use{RESET}")

    # Check if the quantize_version is valid
    while True:
        try:
            if language == 2:
                quantize_version = input(f"{GREEN}\nVeuillez entrer la quantize version que vous souhaitez utiliser pour la quantification :\n{RESET}")
            else: 
                quantize_version = input(f"{GREEN}\nPlease enter the quantize version you want to use for quantization :\n{RESET}")
            subprocess.run(["docker", "run", "--rm", "-v", ".:/model", "ollama/quantize", "-q", quantize_version, "/model"], check=True)
            
            # Ask the user if they want to continue quantizing
            if language == 2:
                continue_quantizing = input(f"{GREEN}\nSi vous voulez quantize à nouveau, tapez 1. Sinon, tapez 2 :\n{RESET}")
            else:
                continue_quantizing = input(f"{GREEN}\nIf you want to quantize again, type 1. Otherwise, type 2 :\n{RESET}")
            
            if continue_quantizing not in ['1', '2']:
                print(f"{RED}Veuillez choisir soit 1 ou 2.{RESET}" if language == 2 else f"{RED}Please choose either 1 or 2.{RESET}")
                continue
            elif continue_quantizing == '2':
                break
        except subprocess.CalledProcessError:
            if language == 2:
                print(f"{RED}La quantize version n'est pas valide. Veuillez réessayer.{RESET}")
            else: 
                print(f"{RED}The quantize version is invalid. Try Again.{RESET}")

    while True:
        # Create the Modelfile
        with open('Modelfile', 'w') as f:
            f.write('')

        example_modelfile = """     
FROM ./q4_0.bin\n \
TEMPLATE [INST] {{ .System }} {{ .Prompt }} [/INST]\n \
SYSTEM \"\"\"You are a assistant..\"\"\"\n \
PARAMETER stop \"[INST]\"\n \
PARAMETER stop \"[/INST]\"\n \
"""
        if language == 2:
            print(f"\n{GREEN}Veuillez saisir votre Modelfile pour le modèle quantizé en format Ollama{RESET}")
            print(f"{RED}Attention le Modelfile doit correspondre au Modelfile du Modèle initialement utilisé pour le fine-tune{RESET}")
            print(f"{CYAN}Voici un exemple du Modelfile : {example_modelfile} \n{RESET}")
        else: 
            print(f"\n{GREEN}Please enter your Modelfile for the quantized model in Ollama format{RESET}")
            print(f"{RED}Attention the Modelfile must correspond to the Modelfile of the Model initially used for fine-tune{RESET}")
            print(f"{CYAN}Here an example for the Modelfile : {example_modelfile} \n{RESET}")

        # Set messages according to your chosen language
        if language == 2:
            messages = {
                "edit_message": "\nTapez 1 quand vous avez fini d'éditer le fichier Modelfile :\n",
                "model_message": "\nVeuillez entrer le nom du modèle que vous souhaitez créer :\n"
            }
        else:
            messages = {
                "edit_message": "\nType 1 when you have finished editing the Modelfile :\n",
                "model_message": "\nPlease enter the name of the model you wish to create :\n"
            }

        # Open the file via a text editor
        if platform.system() == 'Windows':
            os.startfile(os.path.abspath('Modelfile'))
        elif platform.system() == 'Linux':
            subprocess.run(["xdg-open", os.path.abspath('Modelfile')])

        # Ask the user to type 1 when finished
        user_input = input(messages["edit_message"])
        while user_input != '1':
            user_input = input(messages["edit_message"])

        if language == 2:
            print(f"{GREEN}Veuillez fermer et quitter Docker maintenant.{RESET}")
            print(f"{CYAN}Tapez 1 une fois que vous avez fermé Docker.{RESET}")
            user_input = input()
            if user_input == '1':
                pass
        else: 
            print(f"{GREEN}Please close and exit Docker now.{RESET}")
            print(f"{CYAN}Type 1 once you have closed Docker.{RESET}")
            user_input = input()
            if user_input == '1':
                pass

        time.sleep(3)
        try:
            subprocess.check_output(["ollama", "serve"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            pass
        else:
            # If 'ollama serve' runs successfully, then run the subprocess
            subprocess.Popen(["start", "cmd", "/k", "ollama", "serve"], shell=True)

        # Ask the user the name of the model they want
        model_name = input(messages["model_message"])

        # Run the ollama create command
        subprocess.run(["ollama", "create", model_name, "--file", os.path.abspath('Modelfile')])
        if language == 2:
            print(f"{GREEN}Modèle construit avec succès !{RESET}")
        else: 
            print(f"{GREEN}Model built successfully !{RESET}")

        # Read the contents of the Modelfile
        with open('Modelfile', 'r') as f:
            content = f.read()

        # Use a regular expression to find the file name
        match = re.search(r'FROM ./([\w.]+)', content)
        if match:
            file_name = match.group(1)
            if os.path.exists(file_name):
                print(f"Le fichier {file_name} a été trouvé." if language == 2 else f"File {file_name} was found.")
                os.remove(file_name)
                print(f"Le fichier {file_name} a été supprimé." if language == 2 else f"File {file_name} has been deleted.")
            else:
                print(f"Le fichier {file_name} n'a pas été trouvé." if language == 2 else f"The file {file_name} was not found.")
        else:
            print("Aucun nom de fichier trouvé dans Modelfile." if language == 2 else "No filename found in Modelfile.")
            pass

        # Ask the user if they want to build another model
        if language == 2:
            user_input = input(f"{GREEN}Voulez-vous construire un autre modèle ? Tapez 1 pour Oui, 2 pour Non :\n{RESET}")
        else: 
            user_input = input(f"{GREEN}Do you want to build another model? Type 1 for Yes, 2 for No :{RESET}")
        while user_input not in ['1', '2']:
            print(f"{RED}Veuillez choisir une option valide.{RESET}" if language == 2 else f"{RED}Please choose a valid option.{RESET}")
            if language == 2:
                user_input = input(f"{GREEN}Voulez-vous construire un autre modèle ? Tapez 1 pour Oui, 2 pour Non :{RESET}")
            else: 
                user_input = input(f"{GREEN}Do you want to build another model? Type 1 for Yes, 2 for No :{RESET}")
        if user_input == '2':
            subprocess.run(['explorer', os.path.realpath(os.path.join(model_dir, *subdirs))])
            break


quantize_model_interface()