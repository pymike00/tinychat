import requests

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import COHERE_API_KEY_NAME


class CohereClient(BaseLLMClient):
    """
    Cohere chat client.
    """

    COHERE_CHAT_API_URL = "https://api.cohere.ai/v1/chat"

    def __init__(self) -> None:
        super().__init__(api_key_name=COHERE_API_KEY_NAME)
        self.chat_history = []

    def _update_chat_history(self, user_input: str, answer: str) -> None:
        self.chat_history.append({"role": "User", "message": user_input})
        self.chat_history.append({"role": "Chatbot", "message": answer})

    def _make_api_request(self, user_input: str) -> None:
        data = {
            "chat_history": self.chat_history,
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

    def get_response(self, user_input: str) -> str:
        try:
            chat_response = self._make_api_request(user_input=user_input)
        except ValueError as e:
            return e
        self._update_chat_history(user_input, chat_response)
        return chat_response
