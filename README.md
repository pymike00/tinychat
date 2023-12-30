<div align="center">
<img height="250" src="./tinychat2.png">

<h1>TinyChat</h1>

*A tiny GUI client for modern Language Models*

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

# Run tinychat
cd src
python tinychat.pyw
```

## Supported Models
**Supports all major chat models from OpenAI, Mistral and Cohere official cloud APIs:**

- [X] GPT-4 Turbo
- [X] GPT-3.5-Turbo
- [X] Mixtral 8x7B
- [X] Mistral 7B
- [X] Mistral Medium
- [X] Cohere Chat


## Lots of things to do still

- Support for Chat History
- Support for 
- Better API key handling (currently using a secrets.json)
- Tests, tests, tests.
