import json
from typing import Generator

import requests
from sseclient import SSEClient

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import OPENAI_API_KEY_NAME


class OpenAIClient(BaseLLMClient):
    """
    Simple client for interacting with the OpenAI API.
    Currently only supports the chat completions endpoint.

    :param model_name: The name of the model to be used for chat requests.
    """

    OPENAI_COMPLETION_API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, model_name: str, temperature: float = 1.0) -> None:
        super().__init__(api_key_name=OPENAI_API_KEY_NAME)
        self.model_name = model_name
        self.temperature = temperature

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

    def perform_stream_request(self, messages: list[dict]) -> SSEClient:
        # info: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": True,
        }
        response = requests.post(
            self.OPENAI_COMPLETION_API_URL,
            headers=self.default_headers(),  # type: ignore
            json=data,
            stream=True,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Server responded with an error. Status Code: {response.status_code}"
            )
        return SSEClient(event_source=response)  # type: ignore


class OpenAIHandler:
    """
    Handler class to interact with the OpenAI models.

    Returns chat responses and stores the chat history.
    """

    def __init__(self, model_name: str):
        self._messages = []
        self._client = OpenAIClient(model_name=model_name)

    def get_response(self, user_input: str) -> str:
        """Return complete chat response from client"""
        self._messages.append({"role": "user", "content": user_input})
        chat_response = self._client.perform_chat_request(self._messages)
        self._messages.append({"role": "assistant", "content": chat_response})
        return chat_response

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        """
        Yield stream responses from the client as they are received.

        This method sends the user input to the client and then yields each piece
        of the language model's response as it is received in real-time. After the
        streaming is complete, it updates the message list with the user input and
        the full language model response.

        :param user_input: The input string from the user to be sent to the model.
        :return: A generator yielding the model's response in streamed parts.
        """
        self._messages.append({"role": "user", "content": user_input})
        stream = self._client.perform_stream_request(self._messages)
        lm_response = ""
        for event in stream.events():  # type: ignore
            if event.data != "[DONE]":
                json_load = json.loads(event.data)["choices"][0]["delta"]
                if "content" in json_load.keys():
                    response_piece = json_load["content"]
                    lm_response += response_piece
                    yield response_piece
        self._messages.append({"role": "assistant", "content": lm_response})
