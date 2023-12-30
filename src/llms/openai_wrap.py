from openai import OpenAI as OpenAIClient

from llms.base import BaseLLMWrapper
from settings import OPENAI_API_KEY_NAME


class OpenAIClientWrapper(BaseLLMWrapper):
    """
    OpenAI client wrapper for various language models.
    Currently only supports chat.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo") -> None:
        super().__init__(client=OpenAIClient, api_key_name=OPENAI_API_KEY_NAME)
        self.model_name = model_name
        self.messages = []

    def get_response(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model=self.model_name, messages=self.messages, temperature=1.0  # 0.0 - 2.0
        )
        self.messages.append(response.choices[0].message)
        return response.choices[0].message.content