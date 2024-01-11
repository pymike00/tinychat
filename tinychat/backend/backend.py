from tkinter import filedialog

from tinychat.llms.base import LLMProtocol
from tinychat.llms.cohere import CohereHandler
from tinychat.llms.google import GoogleAIHandler
from tinychat.llms.mistral import MistralHandler
from tinychat.llms.openai import OpenAIHandler


class Backend:
    def __init__(self) -> None:
        self._models = {
            "Language Model ": lambda: None,
            "GPT-4 Turbo": lambda: OpenAIHandler("gpt-4-1106-preview"),
            "GPT-3.5 Turbo": lambda: OpenAIHandler("gpt-3.5-turbo"),
            "Gemini Pro": lambda: GoogleAIHandler(),
            "Mistral Medium": lambda: MistralHandler("mistral-medium"),
            "Mixtral 8X7B": lambda: MistralHandler("mistral-small"),
            "Mistral 7B": lambda: MistralHandler("mistral-tiny"),
            "Cohere Chat": lambda: CohereHandler(),
        }
        self._llm: LLMProtocol = None  # type: ignore

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
            return "No Language Model Has Been Selected."
        return self._llm.get_response(user_input)

    def get_stream_response(self, user_input: str):
        if self._llm is None:
            raise ValueError("No Language Model Has Been Selected.")
        return self._llm.stream_response(user_input)

    def export_conversation(self):
        if self._llm is None:
            return
        new_file = filedialog.asksaveasfilename(
            initialfile="Untitled.txt",
            defaultextension=".txt",
            filetypes=[("File di Testo", "*.txt")],
        )
        with open(new_file, "w") as f:
            f.write(self._llm.export_conversation())


if __name__ == "__main__":
    backend = Backend()
    backend.set_model("GPT-3.5 Turbo")
    while True:
        user_input = input("You: ")
        chat_response = backend.get_chat_response(user_input)
        print(chat_response)
