import requests

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import MISTRAL_API_KEY_NAME


class MistralClientWrapper(BaseLLMClient):
    """
    Mistral chat client.
    """

    MISTRAL_COMPLETION_API_URL = "https://api.mistral.ai/v1/chat/completions"

    def __init__(self, model_name: str = "mistral-tiny") -> None:
        super().__init__(api_key_name=MISTRAL_API_KEY_NAME)
        self.model_name = model_name
        self.messages = []

    def _make_api_request(self) -> str:
        data = {
            "model": self.model_name,
            "messages": self.messages,
            "temperature": self.temperature,
        }
        response = requests.post(
            self.MISTRAL_COMPLETION_API_URL,
            headers=self.default_headers(),
            json=data,
        )
        if response.status_code != 200:
            raise ValueError(f"Server responded with error: {response.status_code}")
        try:
            return response.json()["choices"][0]["message"]["content"]
        except KeyError as e:
            raise KeyError(f"Invalid response format received from server. {e}")

    def get_response(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        try:
            chat_response = self._make_api_request()
        except KeyError as e:
            return e
        self.messages.append({"role": "assistant", "content": chat_response})
        return chat_response
