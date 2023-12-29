from llms.base import LLMProtocol
from llms.cohere_wrap import CohereClientWrapper
from llms.mistral_wrap import MistralClientWrapper
from llms.openai_wrap import OpenAIClientWrapper


class Backend:
    def __init__(self) -> None:
        self._models = {
            "GPT-4 Turbo": lambda: OpenAIClientWrapper("gpt-4-1106-preview"),
            "GPT-3.5 Turbo": lambda: OpenAIClientWrapper("gpt-3.5-turbo"),
            "Mixtral-8X7B": lambda: MistralClientWrapper("mistral-small"),
            "Mistral-7B": lambda: MistralClientWrapper("mistral-tiny"),
            "Mixtral Medium": lambda: MistralClientWrapper("mistral-medium"),
            "Cohere Chat": lambda: CohereClientWrapper(),
        }
        self._llm: LLMProtocol = self._models["GPT-4 Turbo"]()

    def available_models(self) -> list:
        return list(self._models.keys())
    
    def set_model(self, model_name: str) -> None:
        if model_name not in self.available_models():
            raise KeyError("Invalid Model Name")
        self._llm = self._models[model_name]()

    def get_chat_response(self, user_input: str) -> str:
        return self._llm.get_response(user_input)


if __name__ == "__main__":
    backend = Backend()
    while True:
        user_input = input("You: ")
        chat_response = backend.get_chat_response(user_input)
        print(chat_response)
