import requests

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import COHERE_API_KEY_NAME


class CohereClient(BaseLLMClient):
    """
    Cohere chat client.
    """

    COHERE_CHAT_API_URL = "https://api.cohere.ai/v1/chat"

    def __init__(self, temperature: float = 1.0) -> None:
        super().__init__(api_key_name=COHERE_API_KEY_NAME)
        self.temperature = temperature

    def perform_chat_request(self, user_input: str, chat_history: list[dict]) -> str:
        data = {
            "chat_history": chat_history,
            "message": user_input,
            "temperature": self.temperature,
        }
        response = requests.post(
            self.COHERE_CHAT_API_URL,
            headers=self.default_headers(),
            json=data,
        )
        if response.status_code != 200:
            raise ValueError(f"Server responded with error: {response.status_code}")
        try:
            return response.json().get("text", "No response text found")
        except ValueError:
            raise ValueError("Invalid response format received from server.")


class CohereHandler:
    """
    Handler class to interact with the Cohere models.

    Returns chat responses and stores the chat history.

    TODO: add chat message dataclass so that we can enforce validation of
    message format that is needed for working client requests to the API?
    """

    def __init__(self):
        self._chat_history = []
        self._client = CohereClient()

    def _update_chat_history(self, user_input: str, answer: str) -> None:
        self._chat_history.append({"role": "User", "message": user_input})
        self._chat_history.append({"role": "Chatbot", "message": answer})

    def get_response(self, user_input: str) -> str:
        chat_response = self._client.perform_chat_request(
            user_input, self._chat_history
        )
        self._update_chat_history(user_input, chat_response)
        return chat_response
