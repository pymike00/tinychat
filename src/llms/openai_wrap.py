from openai import OpenAI as OpenAIClient

from llms.base import BaseLLMWrapper


class OpenAIClientWrapper(BaseLLMWrapper):
    """
    OpenAI client wrapper for various language models.
    Currently only supports chat.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo") -> None:
        super().__init__(client=OpenAIClient, api_key_name="openai_api_key")
        self.model_name = model_name
        self.messages = []

    def get_response(self, user_input: str) -> str:
        self.messages.append({
            "role": "user", "content": user_input
        })
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages=self.messages,
            temperature = 1.0 # 0.0 - 2.0
        )
        self.messages.append(response.choices[0].message)
        return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage:
    model_name = "gpt-3.5-turbo"
    user_input = "Hello, who are you?"
    client_wrapper = OpenAIClientWrapper(model_name=model_name)
    response = client_wrapper.get_response(user_input)
    print(f"Response from the model: {response}")