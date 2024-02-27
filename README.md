# TinyChat

**TinyChat is a GUI client for modern Language Models built with simplicity in mind. Its minimalistic Python code is designed for straightforward comprehension and adaptability. More features will likely come, but we are going to do our best to keep it simple.**

To reduce magic to a minimum, no official API client is used: it's only just post requests and Server-Sent Events handling. The program only depends on [requests](https://requests.readthedocs.io/en/latest/), [sseclient-py](https://github.com/mpetazzoni/sseclient) and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

**You can talk with all major models from the OpenAI, Mistral, Google and Cohere cloud APIs:**
- [x] GPT-4 Turbo
- [x] GPT-3.5-Turbo
- [x] Mixtral 8x7B
- [x] Mistral 7B
- [x] Mistral Large, Medium and Small
- [x] Gemini Pro
- [x] Cohere Chat


### Here is a quick demo:
https://github.com/pymike00/tinychat/assets/32687496/aec0cfb4-de53-4399-b952-b1c636194718

### Notes:
- *To use the models you will need an API Key from [OpenAI](https://platform.openai.com/api-keys) / [Mistral](https://console.mistral.ai/user/api-keys/) / [Google](https://makersuite.google.com/app/apikey) / [Cohere](https://dashboard.cohere.com/api-keys/). Follow the links to get started! The keys will be saved in a "tinychat.json" file that by default is created on the same level as the tinychat package / exe file. You can change the SECRETS_FILE_PATH from the settings.py file.*
- *I chose to use the official Mistral API and not something like TogheterAI to explicitly support Mistral's open weights strategy. You should however be able to easily adapt the code in llms.mistral to change the endpoint in case you feel like it.*

<br>

### How to use it as a Python package:


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


### How to build an executable:


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

### Extra Notes:
[Crystal ball icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/crystal-ball)

