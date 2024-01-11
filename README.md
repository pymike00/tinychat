<div align="center">
<img style="max-height:300px" style="border-radius: 3%;" src="./assets/tinychat.jpg">

<h1>TinyChat</h1>

*A simple GUI client for modern Language Models*

**TinyChat is built with simplicity in mind. Its minimalistic Python code is designed for straightforward comprehension. More features will likely come, but it will stay tiny. Promised!**
</div>
<br>


### Here is a quick demo:
https://github.com/pymike00/tinychat/assets/32687496/aec0cfb4-de53-4399-b952-b1c636194718

<br>

### You can either use it as a Python package:


```
# Clone repo and enter main folder
git clone https://github.com/pymike00/tinychat.git
cd tinychat

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment
source venv/bin/activate on Linux / Mac OS
.\venv\Scripts\Activate.ps1 on Windows Powershell

# Install requirements
pip install -r requirements.txt

# Run application
python -m tinychat
```

<br>

### Or you can build an executable. I will release some builds in the very near future:


```
# Clone repo and enter main folder
git clone https://github.com/pymike00/tinychat.git
cd tinychat

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment
source venv/bin/activate on Linux / Mac OS
.\venv\Scripts\Activate.ps1 on Windows Powershell

# Install requirements
pip install -r requirements-build.txt

# Run build commands
pyinstaller build.spec

# You should now have a new tinychat executable file in a newly created dist folder
```
<br>

### Select your favorite model and start chatting
**You can talk with all major models from the OpenAI, Mistral, Google and Cohere cloud APIs:**

- [x] GPT-4 Turbo
- [x] GPT-3.5-Turbo
- [x] Mixtral 8x7B
- [x] Mistral 7B
- [x] Mistral Medium
- [x] Gemini Pro
- [x] Cohere Chat

*To use the models you will need an API Key from [OpenAI](https://platform.openai.com/api-keys) / [Mistral](https://console.mistral.ai/user/api-keys/) / [Google](https://makersuite.google.com/app/apikey) / [Cohere](https://dashboard.cohere.com/api-keys/). Follow the links to get started! We chose to use the official Mistral API and not something like TogheterAI to explicitly support Mistral's open weights strategy. We will however implement a setting to change the API endpoints for those models arbitrarily soon.*



<br>

### Dependency - less
By making direct HTTP requests to the API endpoints, no official client needs to be installed. TinyChat only depends on [requests](https://requests.readthedocs.io/en/latest/), [sseclient-py](https://github.com/mpetazzoni/sseclient) and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).


<br>

### Roadmap:

- Chat history
- Multimodality
- Support for local models

<br>

[Crystal ball icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/crystal-ball)
