import json
from typing import Any, Protocol


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


class BaseLLMWrapper:
    """
    Base wrapper class for language model clients.
    """

    def __init__(self, client: Any, api_key_name: str) -> None:
        self.client = self._init_client(client, api_key_name)

    def _init_client(self, client: Any, api_key_name: str) -> Any:
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                api_key = secrets[api_key_name]
        except FileNotFoundError:
            raise FileNotFoundError("The file 'secrets.json' was not found.")
        except KeyError:
            raise KeyError(f"The '{api_key_name}' was not found in 'secrets.json'.")
        return client(api_key=api_key)