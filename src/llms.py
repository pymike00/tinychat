import json
from typing import Protocol, Union

from cohere import Client as CohereClient
from openai import OpenAI as OpenAIClient


class LLMProtocol(Protocol):
    """
    A protocol for language model clients.
    This can be implemented by any class that acts as a wrapper around
    language model APIs such as Cohere or OpenAI.
    """

    def _init_client(self) -> Union[CohereClient, OpenAIClient]:
        """
        Initialize and return a language model client.
        This method can return either a Cohere client or an OpenAI client.
        """
        ...

    def get_response(self, user_input: str) -> str:
        """
        Get a response from the language model.
        This method should be implemented to interact with the underlying
        language model (Cohere or OpenAI) and return a response string.
        """
        ...


class CohereChat:

    def __init__(self) -> None:
        self.chat_history = []
        self.client = self._init_client()

    def _init_client(self) -> CohereClient:
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                api_key = secrets["cohere_api_key"]
        except FileNotFoundError:
            raise FileNotFoundError("The file 'secrets.json' was not found.")
        except KeyError:
            raise KeyError("The 'cohere_api_key' was not found in 'secrets.json'.")
        return CohereClient(api_key=api_key)

    def get_response(self, user_input: str) -> str:
        response = self.client.chat(
            chat_history=self.chat_history,
            message=user_input,
            temperature=1
        )
        answer = response.text
        self.chat_history.append({"role": "User", "message": user_input})
        self.chat_history.append({"role": "Chatbot", "message": answer})
        return answer


class GPT35Turbo:

    def __init__(self) -> None: 
        self.messages = [
            {
                "role": "system", 
                "content": "You are a helpful programming assistant."
            }
        ]
        self.client = self._init_client()

    def _init_client(self) -> OpenAIClient:
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                api_key = secrets["openai_api_key"]
        except FileNotFoundError:
            raise FileNotFoundError("The file 'secrets.json' was not found.")
        except KeyError:
            raise KeyError("The 'openai_api_key' was not found in 'secrets.json'.")
        return OpenAIClient(api_key=api_key)

    def get_response(self, user_input: str) -> str:
        self.messages.append({
            "role": "user", "content": user_input
        })
        response = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=self.messages,
            temperature = 1.0 # 0.0 - 2.0
        )
        self.messages.append(response.choices[0].message)
        return response.choices[0].message.content