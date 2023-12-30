from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from llms.base import BaseLLMWrapper
from settings import MISTRAL_API_KEY_NAME


class MistralClientWrapper(BaseLLMWrapper):
    """
    Mistral chat client.
    """

    def __init__(self, model_name: str = "mistral-small") -> None:
        super().__init__(client=MistralClient, api_key_name=MISTRAL_API_KEY_NAME)
        self.model_name = model_name
        self.messages = []

    def get_response(self, user_input: str) -> str:
        self.messages.append(ChatMessage(role="user", content=user_input))
        response = self.client.chat(
            model=self.model_name, messages=self.messages, temperature=1.0
        )
        answer = response.choices[0].message.content
        self.messages.append(response.choices[0].message)
        return answer
