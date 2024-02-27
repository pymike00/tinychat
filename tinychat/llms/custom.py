from typing import Generator

from llama_cpp import Llama


class CustomHandler:
    """
    Handler class to interact with custom GGUF models.

    Returns chat responses and stores the chat history.
    """

    def __init__(self, model_name: str):
        self._messages = []
        self.llm = Llama(model_path=model_name, n_gpu_layers=-1)
    
    def export_conversation(self) -> str:
        string_conversation = ""
        for message in self._messages:
            if message["role"] == "user":
                if string_conversation != "":
                    string_conversation += "\n\n"
                string_conversation += f"You: {message['content']}"
            else:
                string_conversation += f"LLM: {message['content']}"
        return string_conversation

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        self._messages.append({"role": "user", "content": user_input})
        lm_response = ""
        stream = self.llm.create_chat_completion(
            messages=[
                {"role": "user", "content": user_input},
            ],
            stream=True,
            temperature=1.0
        )
        for piece in stream:
            if "content" in piece["choices"][0]["delta"].keys():
                yield piece["choices"][0]["delta"]["content"]
        self._messages.append({"role": "assistant", "content": lm_response})