APP_VERSION = "0.8.2"

# Title for the main GUI window of the application
MAIN_WINDOW_TITLE = f"NDA Reviewer"

# Resolution for the main GUI window of the application (e.g. 1440x900)
MAIN_WINDOW_RESOLUTION = "1200x750"

# Set font-family
FONT_FAMILY = "Inter"

# API Key storage file location
SECRETS_FILE_PATH = "nda_reviewer.json"

# API Key Constants. Used as names in the API Key storage file
OPENAI_API_KEY_NAME = "OPENAI_API_KEY"

import os, sys

def get_icon_path():
    if os.name == "nt":
        icon_file_name = "nda_reviewer.ico"
    else:
        icon_file_name = "nda_reviewer.png"
    if not hasattr(sys, "frozen"):
        return os.path.join(os.path.dirname(__file__), icon_file_name)
    else:
        return os.path.join(sys.prefix, icon_file_name)