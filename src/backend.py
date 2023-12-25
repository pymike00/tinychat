from llms import CohereChat, GPT35Turbo, LLMProtocol


class Backend:
    def __init__(self) -> None:
        self._llm: LLMProtocol = GPT35Turbo()
        self._models = {
            "GPT-3.5 Turbo": GPT35Turbo,
            "Cohere Chat": CohereChat
            # Add other models as needed
        }

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
