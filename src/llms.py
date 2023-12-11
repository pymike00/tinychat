import json
from typing import Protocol

import cohere
from openai import OpenAI


class LLMProtocol(Protocol):

    def init_client(self, *args, **kwargs) -> None:
        ...

    def get_response(self, user_input: str) -> str:
        ...


class CohereChat:

    def __init__(self):
        self.chat_history = []

    def init_client(self):
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                api_key = secrets["cohere_api_key"]
            self.client = cohere.Client(api_key=api_key)
        except FileNotFoundError:
            raise FileNotFoundError("The file 'secrets.json' was not found.")
        except KeyError:
            raise KeyError("The 'cohere_api_key' was not found in 'secrets.json'.")

    def get_response(self, user_input: str):
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

    def __init__(self):
        self.messages = [
            {
                "role": "system", 
                "content": "You are a helpful programming assistant."
            }
        ]

    def init_client(self):
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                api_key = secrets["openai_api_key"]
            self.client = OpenAI(api_key=api_key)
        except FileNotFoundError:
            raise FileNotFoundError("The file 'secrets.json' was not found.")
        except KeyError:
            raise KeyError("The 'openai_api_key' was not found in 'secrets.json'.")

    def get_response(self, user_input: str):
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