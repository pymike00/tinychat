import requests

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import GOOGLE_API_KEY_NAME


class GoogleGeminiClient(BaseLLMClient):
    """
    Simple client for interacting with the Google API.
    Currently only supports the chat completions endpoint.

    :param model_name: The name of the model to be used for chat requests.
    """

    BASE_GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def __init__(self) -> None:
        super().__init__(api_key_name=GOOGLE_API_KEY_NAME)

    @property
    def gemini_endpoint(self):
        return f"{self.BASE_GEMINI_ENDPOINT}?key={self.api_key}"

    @property
    def gemini_headers(self):
        return {"Content-Type": "application/json"}

    def perform_chat_request(self, messages: list[dict]) -> str:
        data = {"contents": messages}
        response = requests.post(
            self.gemini_endpoint,
            headers=self.gemini_headers,  # type: ignore
            json=data,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Server responded with an error. Status Code: {response.status_code}"
            )
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError as e:
            raise KeyError(f"Invalid response format received from server. {e}")


class GoogleGeminiHandler:
    """
    Handler class to interact with the OpenAI models.

    Returns chat responses and stores the chat history.

    TODO: add chat message dataclass so that we can enforce validation of
    message format that is needed for working client requests to the API?
    """

    def __init__(self):
        self._messages = []
        self._client = GoogleGeminiClient()

    def get_response(self, user_input: str) -> str:
        self._messages.append({"parts": [{"text": user_input}], "role": "user"})
        chat_response = self._client.perform_chat_request(self._messages)
        self._messages.append({"parts": [{"text": chat_response}], "role": "model"})
        return chat_response
