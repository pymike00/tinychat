# NDA Reviewer (for Linux and Windows)

**NDA Reviewer is a GUI application designed to streamline the process of reviewing and revising Non-Disclosure Agreements (NDAs). Built with simplicity in mind, its minimalistic Python code is designed for straightforward comprehension and adaptability.**

This application leverages modern Language Models to assist in the analysis and revision of NDAs. It provides an intuitive interface for uploading NDAs and guidelines, analyzing the documents, and reviewing suggested changes.

Key features include:
- Upload and manage NDAs and guidelines
- Automated analysis and revision suggestions
- Interactive review of proposed changes
- Download revised NDAs
- Support for multiple AI models for diverse analysis capabilities

### Supported AI Models:
- OpenAI: GPT-4, GPT-4 Turbo
- Anthropic: Claude 3.5 Sonnet, Claude 3 Opus
- Mistral: Large, Codestral
- Meta AI: Llama3 8B, Llama3 70B
- Google: Gemini Pro 1.5
- Cohere: Command R

### How to use the application:

1. Upload your NDA and guidelines
2. Select an AI model for analysis
3. Initiate the analysis and revision process
4. Review suggested changes interactively
5. Apply approved changes
6. Download the revised NDA

### Installation and Setup:

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

### Building an Executable:

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

### Notes:
- To use the AI models, you will need API keys from their respective providers. Please refer to each provider's documentation for obtaining API keys.
- API keys are securely stored in a local JSON file.

This application is designed to assist in the NDA review process but should not replace professional legal advice. Always consult with a qualified legal professional for final review and approval of legal documents.