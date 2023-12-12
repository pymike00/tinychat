from llms import CohereChat, GPT35Turbo, LLMProtocol


class Backend:
    def __init__(self) -> None:
        self._llm: LLMProtocol = GPT35Turbo()
        self.models = {
            "GPT-3.5 Turbo": GPT35Turbo,
            "Cohere Chat": CohereChat
            # Add other models as needed
        }
    
    def _set_llm(self, llm: LLMProtocol) -> None:
        """Set the language model."""
        self._llm = llm

    def available_models(self) -> list:
        return list(self.models.keys())
    
    def set_model(self, model_name) -> None:
        if model_name not in self.models.keys():
            raise KeyError("Invalid Model Name")
        self._set_llm(self.models[model_name]())

    def get_chat_response(self, user_input: str) -> str:
        return self._llm.get_response(user_input)


if __name__ == "__main__":
    try:
        llm = GPT35Turbo()
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
    else:
        backend = Backend()
        while True:
            user_input = input("You: ")
            chat_response = backend.get_chat_response(user_input)
            print(chat_response)
