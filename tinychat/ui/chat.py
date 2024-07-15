import os
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from tinychat.settings import FONT_FAMILY, MAIN_WINDOW_RESOLUTION, MAIN_WINDOW_TITLE
from tinychat.ui.frames import SettingsFrame

class ChatApp(ctk.CTk):
    def __init__(self, backend) -> None:
        super().__init__()

        # Initialize font object to use with the chat text areas
        chat_font = ctk.CTkFont(family=FONT_FAMILY, size=14)

        # Initialize the backend object
        self.backend = backend

        # Initialize the main window
        self.title(MAIN_WINDOW_TITLE)
        self.geometry(MAIN_WINDOW_RESOLUTION)

        # Initialize choices frame with widgets for model selection
        self.settings_frame = SettingsFrame(
            self,
            available_models=backend.available_models(),
            on_model_select_callback=self.on_model_selection,
            on_reset_callback=self.on_reset_callback,
            on_export_callback=self.on_export_callback,
            corner_radius=0,
            fg_color="transparent",
        )
        self.settings_frame.grid(row=0, column=0, rowspan=1, sticky="nsew")

        # Create a text widget to display chat messages
        self.chat_display = ctk.CTkTextbox(
            self,
            font=chat_font,
            wrap=ctk.WORD,
            state="disabled",
        )
        self.chat_display.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Create a smaller text area for typing messages
        self.message_input = ctk.CTkTextbox(
            self, font=chat_font, wrap="word", border_spacing=5
        )
        self.message_input.grid(row=2, column=0, padx=20, pady=(0, 0), sticky="nsew")

        # Add a new frame for the send button and NDA-related buttons
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.bottom_frame.grid_columnconfigure(4, weight=1)
        self.bottom_frame.configure(fg_color="transparent")

        # Upload NDA button
        self.upload_nda_button = ctk.CTkButton(
            self.bottom_frame,
            text="Upload NDA",
            command=self.upload_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.upload_nda_button.grid(row=0, column=0, padx=5, pady=10)

        # Upload Guidelines button
        self.upload_guidelines_button = ctk.CTkButton(
            self.bottom_frame,
            text="Upload Guidelines",
            command=self.upload_guidelines,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.upload_guidelines_button.grid(row=0, column=1, padx=5, pady=10)

        # Analyze and Revise NDA button
        self.analyze_button = ctk.CTkButton(
            self.bottom_frame,
            text="Analyze and Revise NDA",
            command=self.analyze_and_revise_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.analyze_button.grid(row=0, column=2, padx=5, pady=10)

        # Download Revised NDA button
        self.download_nda_button = ctk.CTkButton(
            self.bottom_frame,
            text="Download Revised NDA",
            command=self.download_revised_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.download_nda_button.grid(row=0, column=3, padx=5, pady=10)

        # Create a button for sending messages
        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="Send",
            command=self.send_message_thread,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.send_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

        # Set focus (cursor) to message_input automatically
        self.after(100, lambda: self.message_input.focus_set())

        # Configure the grid layout
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Bind Enter key press to send_message action
        self.bind("<Return>", self.on_enter)

        # Bind (CTRL or Shift) + Return to do nothing, so we can use to add space
        self.bind("<Control-Return>", self.on_control_enter)
        self.bind("<Shift-Return>", self.on_control_enter)

        # Set the default model to GPT-4
        self.set_initial_model()

    def on_control_enter(self, event) -> None:
        # Handle Control + Enter key event
        # You can leave this empty or add some other functionality
        pass

    def on_shift_enter(self, event) -> None:
        # Handle Shift + Enter key event
        # You can leave this empty or add some other functionality
        pass

    def on_enter(self, event) -> None:
        if self.message_input.get("1.0", tk.END).isspace():
            return
        self.send_message_thread()

    def on_model_selection(self, model_name) -> None:
        try:
            self.model_name = model_name
            self.backend.set_model(model_name=model_name)
        except (KeyError, ValueError) as e:
            self.update_chat_display(message=f"\n{e}")
        else:
            self.clear_chat()

    def on_reset_callback(self) -> None:
        self.clear_chat()
        self.backend.set_model(model_name=self.model_name)

    def on_export_callback(self) -> None:
        threading.Thread(target=self.backend.export_conversation, daemon=True).start()

    def run(self) -> None:
        # start w/ fullscreen https://github.com/TomSchimansky/CustomTkinter/discussions/1500
        self._state_before_windows_set_titlebar_color = "zoomed"

        # Start the application
        self.mainloop()

    def send_message_thread(self) -> None:
        threading.Thread(target=self.send_message, daemon=True).start()

    def send_message(self) -> None:
        user_message = self.message_input.get("1.0", tk.END).strip()
        if user_message:
            self.update_chat_display(message=f"\nYou: {user_message}")
            self.message_input.delete("1.0", tk.END)
            self.send_button.configure(state="disabled")

            try:
                response = self.backend.send_message(user_message)
                self.update_chat_display(message=f"\nAssistant: {response}")
            except Exception as e:
                self.update_chat_display(message=f"\nError: {str(e)}")
            finally:
                self.send_button.configure(state="normal")

    def update_chat_display(self, message: str) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, message)
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)

    def clear_chat(self) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.configure(state="disabled")
        self.message_input.delete("1.0", tk.END)

    def upload_nda(self):
        try:
            result = self.backend.upload_nda()
            tk.messagebox.showinfo("Upload NDA", result)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def upload_guidelines(self):
        try:
            result = self.backend.upload_guidelines()
            tk.messagebox.showinfo("Upload Guidelines", result)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def download_revised_nda(self):
        try:
            result = self.backend.download_revised_nda()
            tk.messagebox.showinfo("Download Revised NDA", result)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def analyze_and_revise_nda(self):
        try:
            result = self.backend.analyze_and_revise_nda()
            if result == "Analysis complete. Ready to review changes.":
                self.review_changes()
            else:
                tk.messagebox.showinfo("Analyze and Revise NDA", result)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def review_changes(self):
        approved_changes = []
        for change in self.backend.review_changes():
            response = tk.messagebox.askyesno(
                "Review Change",
                f"Paragraph {change['paragraph_number']}:\n\nOriginal: {change['original_text']}\n\nSuggested: {change['suggested_change']}\n\nAccept this change?"
            )
            if response:
                approved_changes.append(change)
        
        result = self.backend.apply_approved_changes(approved_changes)
        tk.messagebox.showinfo("Changes Applied", result)

    def set_initial_model(self):
        initial_model = self.settings_frame.model_selection.get()
        self.model_name = initial_model
        self.backend.set_model(model_name=initial_model)