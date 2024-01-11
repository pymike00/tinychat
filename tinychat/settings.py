# Title for the main GUI window of the application
MAIN_WINDOW_TITLE = "TinyChat LM Client"

# Resolution for the main GUI window of the application (e.g. 1440x900)
MAIN_WINDOW_RESOLUTION = "1200x700"

# Set font-family
FONT_FAMILY = "Verdana"  # Consolas

# API Key storage file location
SECRETS_FILE_PATH = "tinychat.json"

# API Key Constants. Used as names in the API Key storage file
OPENAI_API_KEY_NAME = "OPENAI_API_KEY"
MISTRAL_API_KEY_NAME = "MISTRAL_API_KEY"
COHERE_API_KEY_NAME = "COHERE_API_KEY"
GOOGLE_API_KEY_NAME = "GOOGLE_API_KEY"


import os, sys

def get_icon_path():
    icon_file_path = "tinychat.ico"
    if not hasattr(sys, "frozen"):
        return os.path.join(os.path.dirname(__file__), icon_file_path)
    else:
        return os.path.join(sys.prefix, icon_file_path)
