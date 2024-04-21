APP_VERSION = "0.8.0"

# Title for the main GUI window of the application
MAIN_WINDOW_TITLE = f"TinyChat LLM Client - v{APP_VERSION}"

# Resolution for the main GUI window of the application (e.g. 1440x900)
MAIN_WINDOW_RESOLUTION = "1200x750"

# Set font-family
FONT_FAMILY = "Verdana"  # Consolas

# API Key storage file location
SECRETS_FILE_PATH = "tinychat.json"

# API Key Constants. Used as names in the API Key storage file
ANTHROPIC_API_KEY_NAME = "ANTHROPIC_API_KEY"
COHERE_API_KEY_NAME = "COHERE_API_KEY"
GOOGLE_API_KEY_NAME = "GOOGLE_API_KEY"
MISTRAL_API_KEY_NAME = "MISTRAL_API_KEY"
OPENAI_API_KEY_NAME = "OPENAI_API_KEY"
TOGETHER_API_KEY_NAME = "TOGETHER_API_KEY"


import os, sys

def get_icon_path():
    if os.name == "nt":
        icon_file_name = "tinychat.ico"
    else:
        icon_file_name = "tinychat.png"    
    if not hasattr(sys, "frozen"):
        return os.path.join(os.path.dirname(__file__), icon_file_name)
    else:
        return os.path.join(sys.prefix, icon_file_name)
