from typing import Any, Protocol

from tinychat.utils.api_keys import get_api_key
from tinychat.settings import SECRETS_FILE_PATH


class LLMProtocol(Protocol):
    """
    A protocol for language model clients.
    This can be implemented by any class that acts as a wrapper around
    language model APIs such as Cohere or OpenAI.
    """

    def get_response(self, user_input: str) -> str:
        """
        Get a response from the language model.
        This method should be implemented to interact with the underlying
        language model (Cohere or OpenAI) and return a response string.
        """
        ...


class BaseLLMClient:
    """
    A base client class for interacting with Language Model APIs.

    :param api_key: The API key used for authenticating with the API.
    :param temperature: The temperature setting for the language model.
    """

    def __init__(self, api_key_name: str) -> None:
        self.api_key = api_key_name
        self.temperature = 1.0

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key_name):
        api_key = get_api_key(api_key_name)
        if not api_key:
            raise ValueError(f"{api_key_name} was not found in {SECRETS_FILE_PATH}.")
        self._api_key = api_key

    def default_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }



