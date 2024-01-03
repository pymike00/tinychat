import json

from tinychat.settings import SECRETS_FILE_PATH


def load_api_keys(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(file_path, "w") as file:
            json.dump({}, file)
        return {}


def set_api_key(key: str, value: str) -> None:
    secrets = load_api_keys(SECRETS_FILE_PATH)
    secrets[key] = value
    with open(SECRETS_FILE_PATH, "w") as file:
        json.dump(secrets, file, indent=4)  # Writing back the updated secrets


def get_api_key(key: str) -> str:
    secrets = load_api_keys(SECRETS_FILE_PATH)
    return secrets.get(key, "")
