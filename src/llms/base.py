from typing import Any, Protocol

from api_keys import get_api_key
from settings import SECRETS_FILE_PATH


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
        api_key = get_api_key(api_key_name)
        if not api_key:
            raise ValueError(f"{api_key_name} was not found in {SECRETS_FILE_PATH}.")
        return client(api_key=api_key)
