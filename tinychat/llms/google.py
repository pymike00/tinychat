import json
from typing import Generator

import requests
from sseclient import SSEClient

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import GOOGLE_API_KEY_NAME


class GoogleAIClient(BaseLLMClient):
    """
    Simple client for interacting with the Google API.
    Currently only supports the chat completions endpoint.

    :param model_name: The name of the model to be used for chat requests.
    """

    BASE_GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:streamGenerateContent"
    SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
    ]

    def __init__(self, temperature: float) -> None:
        super().__init__(api_key_name=GOOGLE_API_KEY_NAME)
        self.generation_config = {
            "stopSequences": ["Title"],
            "temperature": temperature,
            "maxOutputTokens": 4096,
            "topP": 0.8,
            "topK": 10,
        }

    @property
    def gemini_endpoint(self):
        return f"{self.BASE_GEMINI_ENDPOINT}?alt=sse&key={self.api_key}"

    @property
    def gemini_headers(self):
        return {"Content-Type": "application/json"}

    def perform_stream_request(self, messages: list[dict]) -> SSEClient:
        # info: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
        data = {
            "contents": messages,
            "safetySettings": self.SAFETY_SETTINGS,
            "generationConfig": self.generation_config,
        }
        response = requests.post(
            self.gemini_endpoint,
            headers=self.gemini_headers,  # type: ignore
            json=data,
            stream=True,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Server responded with an error. Status Code: {response.status_code}"
            )
        return SSEClient(event_source=response)  # type: ignore


class GoogleAIHandler:
    """
    Handler class to interact with the Google AI models.

    Returns chat responses and stores the chat history.

    TODO: add chat message dataclass so that we can enforce validation of
    message format that is needed for working client requests to the API?
    """

    def __init__(self, temperature: float = 0.0):
        self._messages = []
        self._client = GoogleAIClient(temperature)

    def export_conversation(self) -> str:
        string_conversation = ""
        for message in self._messages:
            print(message)
            if message["role"] == "user":
                if string_conversation != "":
                    string_conversation += "\n\n"
                string_conversation += f"You: {message['parts'][0]['text']}"
            else:
                string_conversation += f"LLM: {message['parts'][0]['text']}"
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
        self._messages.append({"parts": [{"text": user_input}], "role": "user"})
        stream = self._client.perform_stream_request(self._messages)
        lm_response = ""
        for event in stream.events():  # type: ignore
            event_data = json.loads(event.data)
            # TODO: improve
            if "candidates" in event_data:
                response_piece = event_data["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                lm_response += response_piece
                yield response_piece
        self._messages.append({"parts": [{"text": lm_response}], "role": "model"})
