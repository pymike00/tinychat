import requests

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import MISTRAL_API_KEY_NAME


class MistralClient(BaseLLMClient):
    """
    Mistral chat client.
    """

    MISTRAL_COMPLETION_API_URL = "https://api.mistral.ai/v1/chat/completions"

    def __init__(self, model_name: str, temperature: float = 1.0) -> None:
        super().__init__(api_key_name=MISTRAL_API_KEY_NAME)
        self.model_name = model_name
        self.temperature = temperature

    def perform_chat_request(self, messages: list[dict]) -> str:
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
        }
        response = requests.post(
            self.MISTRAL_COMPLETION_API_URL,
            headers=self.default_headers(),
            json=data,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Server responded with an error. Status Code: {response.status_code}"
            )
        try:
            return response.json()["choices"][0]["message"]["content"]
        except KeyError as e:
            raise KeyError(f"Invalid response format received from server. {e}")


class MistralHandler:
    """
    Handler class to interact with the Mistral models via API.

    Returns chat responses and stores the chat history.

    TODO: add chat message dataclass so that we can enforce validation of
    message format that is needed for working client requests to the API?
    """

    def __init__(self, model_name: str):
        self._messages = []
        self._client = MistralClient(model_name=model_name)

    def get_response(self, user_input: str) -> str:
        self._messages.append({"role": "user", "content": user_input})
        chat_response = self._client.perform_chat_request(self._messages)
        self._messages.append({"role": "assistant", "content": chat_response})
        return chat_response
