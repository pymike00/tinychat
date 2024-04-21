from typing import Optional

from tkinter import filedialog

from tinychat.llms.anthropic import AnthropicAIHandler
from tinychat.llms.base import LLMProtocol
from tinychat.llms.cohere import CohereHandler
from tinychat.llms.google import GoogleAIHandler
from tinychat.llms.mistral import MistralHandler
from tinychat.llms.openai import OpenAIHandler
from tinychat.llms.together import TogetherHandler


class Backend:
    def __init__(self) -> None:
        self.temperature: float = self.get_default_temperature()
        self._models = {
            "Language Model ": lambda: None,
            "GPT-4 Turbo": lambda: OpenAIHandler("gpt-4-turbo-preview", self.temperature),
            "GPT-3.5 Turbo": lambda: OpenAIHandler("gpt-3.5-turbo", self.temperature),
            "Claude 3 Opus": lambda: AnthropicAIHandler("claude-3-opus-20240229", self.temperature),
            "Claude 3 Sonnet": lambda: AnthropicAIHandler("claude-3-sonnet-20240229", self.temperature),
            "Llama3 70B": lambda: TogetherHandler("meta-llama/Llama-3-70b-chat-hf", self.temperature),
            "Llama3 8B": lambda: TogetherHandler("meta-llama/Llama-3-8b-chat-hf", self.temperature),
            "Gemini Pro 1.5": lambda: GoogleAIHandler(self.temperature),
            "Mistral Large": lambda: MistralHandler("mistral-large-latest", self.temperature),
            "Mistral Medium": lambda: MistralHandler("mistral-medium-latest", self.temperature),
            "Cohere Command R": lambda: CohereHandler(self.temperature),
        }
        self._llm: Optional[LLMProtocol] = None

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

    def get_default_temperature(self):
        """
        Get the value of temperature from tinychat.json if available
        else return default_temperature.

        TODO:
        This needs to be actually implemented to be usable from the interface.
        Right now you need to manually add a "temperature": x.x pair in tinychat.json,
        so at the moment it's more like a "secret feature".

        I am adding it to be able to set the temperature after building to exe, as the
        collection of supported models is getting big.

        The idea is to add a slider in frontend to change the value from the actual UI
        https://customtkinter.tomschimansky.com/documentation/widgets/slider/
        However this will probably require a few hours of work and the refactoring
        of several elements of the application to keep everything elegant and simple
        to understand for newcomers.
        """
        from tinychat.utils.secrets import get_secret

        default_temperature = 0.3
        try:
            temperature = float(get_secret("temperature"))
        except ValueError:
            temperature = default_temperature
        return temperature

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
            filetypes=[("Text File", "*.txt")],
        )
        if not new_file:
            return
        with open(new_file, "w") as f:
            f.write(self._llm.export_conversation())
