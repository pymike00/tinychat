from typing import Optional

from tkinter import filedialog

from tinychat.llms.anthropic import AnthropicAIHandler
from tinychat.llms.base import LLMProtocol
from tinychat.llms.cohere import CohereHandler
from tinychat.llms.google import GoogleAIHandler
from tinychat.llms.mistral import MistralHandler
from tinychat.llms.openai import OpenAIHandler
from tinychat.llms.together import TogetherHandler
from tinychat.utils.secrets import get_secret, set_secret


class Backend:
    def __init__(self) -> None:
        self.temperature: float = self.get_default_temperature()
        self._models = {
            "Language Model ": lambda: None,
            "GPT-4o": lambda: OpenAIHandler("gpt-4o", self.temperature),
            "GPT-4 Turbo": lambda: OpenAIHandler("gpt-4-turbo-preview", self.temperature),
            "Claude 3.5 Sonnet": lambda: AnthropicAIHandler("claude-3-5-sonnet-20240620", self.temperature),
            "Claude 3 Opus": lambda: AnthropicAIHandler("claude-3-opus-20240229", self.temperature),
            "Llama 3.1 405B": lambda: TogetherHandler("meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", self.temperature),
            "Llama 3.1 70B": lambda: TogetherHandler("meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", self.temperature),
            "Llama 3.1 8B": lambda: TogetherHandler("meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", self.temperature),
            "Gemini Pro 1.5": lambda: GoogleAIHandler(self.temperature),
            "Mistral Large": lambda: MistralHandler("mistral-large-latest", self.temperature),
            "Mistral Codestral": lambda: MistralHandler("codestral-latest", self.temperature),
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
        """      
        default_temperature = 0.7
        try:
            temperature = float(get_secret("temperature"))
        except ValueError:
            temperature = default_temperature
            set_secret("temperature", default_temperature)
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
