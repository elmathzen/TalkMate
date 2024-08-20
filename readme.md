# TalkMate-AI (for Windows)

Interface allowing you to speak directly with an LLM, record your conversations, speak with an assistant orally, summarize your files and talk about your own data via an integrated RAG system.


## Installation
You can run the **start-app.bat** and follow the installation instructions or do it by hand (in this case see below in the installation tab how to do everything yourself).

**=> Python 3.11.7 (create .env and activate)** you can download here : *https://www.python.org/downloads/release/python-3117/*

**=> Download CUDA 11.8 :**

You can download here CUDA 11.8 : *https://developer.nvidia.com/cuda-11-8-0-download-archive*

```pip3 install torch torchaudio --index-url https://download.pytorch.org/whl/cu118```
- If CUDA don't want to download when you launch the installer becarfull to shutdown all the app that using your GPU (like app Monitor / Monitor Tweak / Msi Afterburner)

- If the installation of pytorch doesn't work, go on : *Install the correct version of pytorch with python & the right version of CUDA for your GPU*

**=> Install librairies :**
```pip install -r requirements.txt```

**=> Need ffmpeg, on Powershell windows :**
- ```iex (new-object net.webclient).downloadstring('https://get.scoop.sh')```
- ```scoop install ffmpeg```

Here ffmeg (an audio-processing library) is used to have Whisper 
(the model to have Speech To Text) and on your computer for download ffmeg we need to have Scoop


**=> Now adding bin of ffmpeg to variable environnements**

Recover the place where your ffmeg is installed :
- Normally it will be in this path : 
    "C:\Users\name_of_the_user_computer\scoop\apps\ffmpeg\version_of_ffmpeg\bin\"

- Click on the Path (on the first 'Path' (your user Path))

- Click on 'New' and put the path of your ffmpeg bin


**=> Download Ollama on your Windows**
Here i use ollama version 0.3.2 for now

- Download Ollama here : **https://ollama.com/download/windows**
- Shutdown the first server that automatically start after the installation on your task bar
- Do on new shell ```ollama serve```
- Do ```ollama pull 'name_of_the_model_you_want_to_download'```

List of Models that i advise you to install : 
- nomic-embed-text (model embedding for vectorization)
- mistral:latest (basic LLM)


## Configuration Synthetic Voices

If you want to have more synthetic voices available, on Windows you have to go to the narrator settings and you can download the voices you want.

If this doesn't work and doesn't recognize the voices you have installed on the narrator settings, follow this steps :
1. Open the **Registry Editor** by pressing the **“Windows” and “R”** keys simultaneously, then type **“regedit”** and press Enter.

2. Navigate to the registry key : **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens**.

3. Export this key to a **REG file** (with a right click on the file).

4. Open this file with a text editor and replace all occurrences of **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens** 
with **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens**.

5. Save the modified file and double-click it to import the changes to the registry.


## Author

- [@nixiz0](https://github.com/nixiz0)
