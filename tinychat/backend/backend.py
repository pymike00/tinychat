from typing import Optional, List
import io
from docx import Document
import os
from tkinter import filedialog
from tkinter import messagebox
import json

from tinychat.llms.base import LLMProtocol
from tinychat.llms.openai import OpenAIHandler
from tinychat.utils.secrets import get_secret, set_secret


class Backend:
    def __init__(self) -> None:
        self.temperature: float = self.get_default_temperature()
        self._models = {
            "Language Model ": lambda: None,
            "OpenAI Assistant": lambda: OpenAIHandler(self.temperature),
        }
        self._llm: Optional[LLMProtocol] = None
        self.uploaded_file_ids = []

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

    def upload_nda(self):
        if not isinstance(self._llm, OpenAIHandler):
            raise ValueError("OpenAI must be selected to use this feature.")
        file_path = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx")])
        if not file_path:
            return "No file selected."
        self.nda_path = file_path
        self.nda_text = self.read_docx(file_path)
        return "NDA uploaded successfully."

    def upload_guidelines(self):
        if not isinstance(self._llm, OpenAIHandler):
            raise ValueError("OpenAI must be selected to use this feature.")
        file_path = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx")])
        if not file_path:
            return "No file selected."
        self.guidelines_text = self.read_docx(file_path)
        return "Guidelines uploaded successfully."

    def analyze_and_revise_nda(self):
        if not isinstance(self._llm, OpenAIHandler):
            raise ValueError("OpenAI must be selected to use this feature.")
        if not hasattr(self, 'nda_path') or not hasattr(self, 'guidelines_text'):
            raise ValueError("Both NDA and guidelines must be uploaded first.")
        
        system_prompt = """You are an AI specialized in reviewing and updating Non-Disclosure Agreements (NDAs) based on specific guidelines. Your task is to analyze the provided NDA, apply the given guidelines only when necessary, and return a list of suggested changes with justifications.

1. Receive Input: You will receive an NDA document and a list of guidelines.
2. Analyze NDA: Carefully read and understand the NDA, identifying relevant sections and clauses.
3. Apply Guidelines: Suggest necessary revisions based on the guidelines. Only suggest edits when required to comply with the guidelines.
4. Return Changes: Provide a list of changes, where each change is an object with the following structure:
   {
     "paragraph_index": int,
     "original_text": str,
     "suggested_text": str,
     "justification": str
   }

Important Considerations:
- Use accurate and appropriate legal terminology.
- Maintain clarity and readability.
- Preserve the structure and format of the original NDA as much as possible.
- Only suggest changes that are necessary to comply with the guidelines.
- Ensure your response is a valid JSON array of change objects."""

        user_input = f"NDA:\n{self.nda_text}\n\nGuidelines:\n{self.guidelines_text}"
        
        try:
            suggested_changes = self._llm.analyze_documents(system_prompt, user_input)
        except ValueError as e:
            print(e)  # Print the full error message to the console
            messagebox.showerror("Error", "The AI response was not in the expected format. Please check the console for more details.")
            return "Analysis failed. Please check the console for more information."

        if not suggested_changes:
            return "No changes suggested by the AI."

        accepted_changes = self.confirm_changes(suggested_changes)
        
        if not accepted_changes:
            return "No changes were accepted."

        revised_doc = self.apply_changes(self.nda_path, accepted_changes)
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx")],
            initialfile="Revised_NDA.docx"
        )
        
        if save_path:
            revised_doc.save(save_path)
            return f"Revised NDA saved successfully to {save_path}"
        else:
            return "File save cancelled by user."

    def confirm_changes(self, suggested_changes: List[dict]) -> List[dict]:
        accepted_changes = []
        for change in suggested_changes:
            message = f"Suggested change:\n\nOriginal: {change['original_text']}\n\nSuggested: {change['suggested_text']}\n\nJustification: {change['justification']}\n\nAccept this change? (y/n): "
            if messagebox.askyesno("Confirm Change", message):
                accepted_changes.append(change)
        return accepted_changes

    def apply_changes(self, original_path: str, changes: List[dict]) -> Document:
        doc = Document(original_path)
        for change in changes:
            paragraph = doc.paragraphs[change['paragraph_index']]
            paragraph.text = change['suggested_text']
        return doc

    def read_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])