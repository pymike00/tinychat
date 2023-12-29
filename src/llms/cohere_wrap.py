from cohere import Client as CohereClient

from llms.base import BaseLLMWrapper


class CohereClientWrapper(BaseLLMWrapper):
    """
    Cohere chat client.
    """

    def __init__(self) -> None:
        super().__init__(client=CohereClient, api_key_name="cohere_api_key")
        self.chat_history = []

    def get_response(self, user_input: str) -> str:
        response = self.client.chat(
            chat_history=self.chat_history, message=user_input, temperature=1
        )
        answer = response.text
        self.chat_history.append({"role": "User", "message": user_input})
        self.chat_history.append({"role": "Chatbot", "message": answer})
        return answer
