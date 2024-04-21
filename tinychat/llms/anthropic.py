import json
from typing import Generator

import requests
from sseclient import SSEClient

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import ANTHROPIC_API_KEY_NAME


class AnthropicAIClient(BaseLLMClient):
    """
    Simple client for interacting with the Anthropic API.
    Currently only supports the messages endpoint.

    :param model_name: The name of the model to be used for chat requests.
    """

    ANTHROPIC_MESSAGES_API_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, model_name: str, temperature: float) -> None:
        super().__init__(api_key_name=ANTHROPIC_API_KEY_NAME)
        self.model_name = model_name
        self.temperature = temperature

    def anthropic_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "messages-2023-12-15",
            "x-api-key": self.api_key,
        }

    def perform_stream_request(self, messages: list[dict]) -> SSEClient:
        # info: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": True,
            "max_tokens": 2048,
        }
        response = requests.post(
            self.ANTHROPIC_MESSAGES_API_URL,
            headers=self.anthropic_headers(),  # type: ignore
            json=data,
            stream=True,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Server responded with an error. Status Code: {response.status_code}"
            )
        return SSEClient(event_source=response)  # type: ignore


class AnthropicAIHandler:
    """
    Handler class to interact with the Anthropic models.

    Returns chat responses and stores the chat history.
    """

    def __init__(self, model_name: str, temperature: float = 0.0):
        self._messages = []
        self._client = AnthropicAIClient(model_name, temperature)

    def export_conversation(self) -> str:
        string_conversation = ""
        for message in self._messages:
            if message["role"] == "user":
                if string_conversation != "":
                    string_conversation += "\n\n"
                string_conversation += f"You: {message['content']}"
            else:
                string_conversation += f"LLM: {message['content']}"
        return string_conversation

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
            event_data = json.loads(event.data)
            if event_data["type"] == "content_block_delta":
                response_piece = event_data["delta"]["text"]
                lm_response += response_piece
                yield response_piece
        self._messages.append({"role": "assistant", "content": lm_response})
