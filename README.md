<div align="center">
<img height="250" src="./assets/tinychat.png">

<h1>TinyChat</h1>

*A simple GUI client for modern Language Models*

**TinyChat is built with simplicity in mind. Its minimalistic Python code is designed for straightforward comprehension. More features will likely come, but it will stay tiny. Promised!**
</div>


## How to Use
**The project was just started, so right now you need to go the developer route**


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

## Important
**Currently, the app does not use response streaming, i.e. the app waits for the whole response to be available before showing the reply. With some models this is fine, as the amounts of token/s provided by the API is very high. Others, such as Mistral's, may be slower. Streaming response is on the TODO list.**

<br>

**Select your favorite model and start chatting**

<img src="./assets/tinychat-two.png">

## Supports all Major Models
**Supports all major chat models from the OpenAI, Mistral, Google and Cohere cloud APIs:**

- [x] GPT-4 Turbo
- [x] GPT-3.5-Turbo
- [x] Mixtral 8x7B
- [x] Mistral 7B
- [x] Mistral Medium
- [x] Gemini Pro
- [x] Cohere Chat

*To use the models you will need an API Key from [OpenAI](https://platform.openai.com/api-keys) / [Mistral](https://console.mistral.ai/user/api-keys/) / [Google](https://makersuite.google.com/app/apikey) / [Cohere](https://dashboard.cohere.com/api-keys/). Follow the links to get started! We chose to use the official Mistral API and not something like TogheterAI to explicitly support Mistral's open weights strategy. We will however implement a setting to change the API endpoints for those models arbitrarily soon.*



<br>

## Dependency - less
By making direct HTTP requests to the API endpoints, no official client needs to be installed. TinyChat only depends on the [requests](https://requests.readthedocs.io/en/latest/) module and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).


<br>

## Project just started. Here is what you can expect for the future:

- [ ] Text formatting in chat textarea
- [ ] Streaming Response?
- [ ] Support for chat history
- [ ] Support for multimodality
- [ ] Support for local models
