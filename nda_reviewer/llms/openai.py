from openai import OpenAI
from typing import Generator, List
import json
from nda_reviewer.utils.secrets import get_secret
from nda_reviewer.settings import OPENAI_API_KEY_NAME

class OpenAIHandler:
    def __init__(self, temperature: float = 0.0):
        # Initialize the OpenAI client with the API key
        self.client = OpenAI(api_key=get_secret(OPENAI_API_KEY_NAME))
        # Set the temperature for generating responses
        self.temperature = temperature
        # Initialize an empty list to store conversation messages
        self.messages = []
        # Set a default system prompt
        self.system_prompt = "You are a helpful assistant."

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        # Add the user's input to the conversation history
        self.messages.append({"role": "user", "content": user_input})
        # Prepare messages for the API call, including the system prompt
        messages_with_system = [{"role": "system", "content": self.system_prompt}] + self.messages
        # Make a streaming API call to OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages_with_system,
            temperature=self.temperature,
            stream=True
        )
        # Initialize a list to collect the response
        collected_messages = []
        # Iterate through the streaming response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                # Collect and yield each part of the response
                collected_messages.append(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content
        # Add the complete assistant's response to the conversation history
        self.messages.append({"role": "assistant", "content": ''.join(collected_messages)})

    def export_conversation(self) -> str:
        # Format the conversation history as a string
        conversation = ""
        for message in self.messages:
            role = "You" if message["role"] == "user" else "Assistant"
            conversation += f"{role}: {message['content']}\n\n"
        return conversation

    def analyze_documents(self, system_prompt: str, user_input: str) -> List[dict]:
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=self.temperature,
        )
        content = response.choices[0].message.content
        print("Raw OpenAI response:")
        print(content)

        # Strip "```json" and brackets from the response
        cleaned_content = content.strip().lstrip('```json').rstrip('```').strip()
        if cleaned_content.startswith('['):
            cleaned_content = cleaned_content[1:]
        if cleaned_content.endswith(']'):
            cleaned_content = cleaned_content[:-1]

        try:
            # Attempt to parse the cleaned content as JSON
            parsed_content = json.loads(f'[{cleaned_content}]')
            return parsed_content
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw content as a single item in a list
            return [{"raw_content": content}]

    def set_system_prompt(self, prompt: str):
        # Update the system prompt
        self.system_prompt = prompt

    def get_response(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        messages_with_system = [{"role": "system", "content": self.system_prompt}] + self.messages
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages_with_system,
            temperature=self.temperature,
        )
        content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})
        return content