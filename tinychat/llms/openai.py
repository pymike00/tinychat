import requests

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import OPENAI_API_KEY_NAME


class OpenAIClient(BaseLLMClient):
    """
    Simple client for interacting with the OpenAI API.
    Currently only supports the chat completions endpoint.

    :param model_name: The name of the model to be used for chat requests.
    """

    OPENAI_COMPLETION_API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, model_name: str) -> None:
        super().__init__(api_key_name=OPENAI_API_KEY_NAME)
        self.model_name = model_name

    def perform_chat_request(self, messages: list[dict]) -> str:
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
        }
        response = requests.post(
            self.OPENAI_COMPLETION_API_URL,
            headers=self.default_headers(),  # type: ignore
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


class OpenAIHandler:
    """
    Handler class to interact with the OpenAI models.

    Returns chat responses and stores the chat history.
    """
    def __init__(self, model_name: str):
        self._messages = []
        self._client = OpenAIClient(model_name=model_name)

    def get_response(self, user_input: str) -> str:
        self._messages.append({"role": "user", "content": user_input})
        chat_response = self._client.perform_chat_request(self._messages)
        self._messages.append({"role": "assistant", "content": chat_response})
        return chat_response
