from tinychat.llms.base import LLMProtocol
from tinychat.llms.cohere_wrap import CohereClientWrapper
from tinychat.llms.mistral_wrap import MistralClientWrapper
from tinychat.llms.openai_wrap import OpenAIClientWrapper


class Backend:
    def __init__(self) -> None:
        self._models = {
            "Select Model": lambda: None,
            "GPT-4 Turbo": lambda: OpenAIClientWrapper("gpt-4-1106-preview"),
            "GPT-3.5 Turbo": lambda: OpenAIClientWrapper("gpt-3.5-turbo"),
            "Mixtral-8X7B": lambda: MistralClientWrapper("mistral-small"),
            "Mistral-7B": lambda: MistralClientWrapper("mistral-tiny"),
            "Mixtral Medium": lambda: MistralClientWrapper("mistral-medium"),
            "Cohere Chat": lambda: CohereClientWrapper(),
        }
        self._llm: LLMProtocol = None

    def available_models(self) -> list:
        return list(self._models.keys())

    def set_model(self, model_name: str) -> None:
        if model_name not in self.available_models():
            raise KeyError(f"Invalid Model Name {model_name}")
        try:
            self._llm = self._models[model_name]()
        except ValueError as e:
            raise ValueError(
                f"Initialization Error. Have you set the API Key for {model_name}? {e}"
            )

    def get_chat_response(self, user_input: str) -> str:
        if self._llm is None:
            return "No LM has been set."
        return self._llm.get_response(user_input)


if __name__ == "__main__":
    backend = Backend()
    backend.set_model("GPT-3.5 Turbo")
    while True:
        user_input = input("You: ")
        chat_response = backend.get_chat_response(user_input)
        print(chat_response)
