import os
import threading
import tkinter as tk

import customtkinter as ctk

from settings import FONT_FAMILY, MAIN_WINDOW_RESOLUTION, MAIN_WINDOW_TITLE


class SettingsFrame(ctk.CTkFrame):
    """
    Allows model selection and access to settings.
    """

    def __init__(
        self, parent, available_models, on_model_select_callback, *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.grid_columnconfigure(2, weight=1)

        # Create model selection menu
        self.model_selection_menu = ctk.CTkOptionMenu(
            self,
            values=available_models,
            command=on_model_select_callback,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
        )
        self.model_selection_menu.grid(
            row=0, column=0, padx=(20, 0), pady=(10, 5), sticky="w"
        )

        # Create settings button
        self.settings_button = ctk.CTkButton(
            self,
            text="Settings",
            command=self.open_settings_window,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
        )
        self.settings_button.grid(
            row=0, column=1, padx=(10, 20), pady=(10, 5), sticky="w"
        )

    def open_settings_window(self):
        # TODO: fix layout and refactor

        # Create a new top-level window for settings
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("API Key Settings")
        settings_window.geometry("600x200")  # Adjusted size to fit API key entries
        settings_window.transient(self)  # Set to be on top of the main window

        # Configure grid layout
        settings_window.grid_columnconfigure(1, weight=1)

        # Add widgets to the settings window for API key entries
        api_key_label_1 = ctk.CTkLabel(settings_window, text="OpenAI API Key: ")
        api_key_label_1.grid(row=0, column=0, padx=(20, 2), pady=(20, 2), sticky="e")
        self.api_key_entry_1 = ctk.CTkEntry(settings_window)
        self.api_key_entry_1.insert(0, os.getenv("OPENAI_API_KEY", ""))
        self.api_key_entry_1.grid(
            row=0, column=1, padx=(2, 20), pady=(20, 2), sticky="ew"
        )

        api_key_label_2 = ctk.CTkLabel(settings_window, text="Mistral API Key: ")
        api_key_label_2.grid(row=1, column=0, padx=(20, 2), pady=(10, 2), sticky="e")
        self.api_key_entry_2 = ctk.CTkEntry(settings_window)
        self.api_key_entry_2.insert(0, os.getenv("MISTRAL_API_KEY", ""))
        self.api_key_entry_2.grid(
            row=1, column=1, padx=(2, 20), pady=(10, 2), sticky="ew"
        )

        api_key_label_3 = ctk.CTkLabel(settings_window, text="Cohere API Key: ")
        api_key_label_3.grid(row=2, column=0, padx=(20, 2), pady=(10, 2), sticky="e")
        self.api_key_entry_3 = ctk.CTkEntry(settings_window)
        self.api_key_entry_3.insert(0, os.getenv("COHERE_API_KEY", ""))
        self.api_key_entry_3.grid(
            row=2, column=1, padx=(2, 20), pady=(10, 2), sticky="ew"
        )

        # Add a close button to the settings window
        close = ctk.CTkButton(
            settings_window, text="Close", command=settings_window.destroy
        )
        close.grid(row=3, column=1, padx=(0, 0), pady=(20, 0), sticky="w")

        # Add a save button to the settings window
        save = ctk.CTkButton(
            settings_window, text="Save Settings", command=self.save_settings
        )
        save.grid(row=3, column=1, padx=(150, 0), pady=(20, 0), sticky="w")

    def save_settings(self):
        os.environ["OPENAI_API_KEY"] = self.api_key_entry_1.get()
        os.environ["MISTRAL_API_KEY"] = self.api_key_entry_2.get()
        os.environ["COHERE_API_KEY"] = self.api_key_entry_3.get()


class ChatApp(ctk.CTk):
    def __init__(self, backend) -> None:
        super().__init__()

        # Initialize font object to use with the chat text areas
        chat_font = ctk.CTkFont(family=FONT_FAMILY, size=15)

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
            corner_radius=0,
            fg_color="transparent",
        )
        self.settings_frame.grid(row=0, column=0, rowspan=1, sticky="nsew")

        # Create a progress bar to enable when getting data from the lms
        self.progress_bar = ctk.CTkProgressBar(self, height=10)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.progress_bar.set(1.0)

        # Create a big text area for displaying chat
        self.chat_display = ctk.CTkTextbox(self, state="disabled", font=chat_font)
        self.chat_display.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Create a smaller text area for typing messages
        self.message_input = ctk.CTkTextbox(self, height=150, font=chat_font)
        self.message_input.grid(row=3, column=0, padx=20, pady=(0, 0), sticky="ew")

        # Create a button for sending messages
        self.send_button = ctk.CTkButton(
            self,
            height=40,
            text="Send Message",
            command=self.on_send_button,
            font=ctk.CTkFont(family=FONT_FAMILY, size=17),
        )
        self.send_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

        # Set focus (cursor) to message_input automatically
        self.after(100, lambda: self.message_input.focus_set())

        # Configure the grid layout
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bind Enter key press to send_message action
        self.bind("<Return>", self.on_enter)

        # Bind (CTRL or Shift) + Return to do nothing, so we can use to add space
        self.bind("<Control-Return>", self.on_control_enter)
        self.bind("<Shift-Return>", self.on_control_enter)

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

    def on_send_button(self) -> None:
        if self.message_input.get("1.0", tk.END).isspace():
            return
        self.send_message_thread()

    def on_model_selection(self, model_name) -> None:
        self.backend.set_model(model_name=model_name)
        self.clear_chat()

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.configure(state="disabled")

    def toggle_progress_bar(self, start: bool):
        if start:
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.set(1.0)

    def send_message_thread(self) -> None:
        threading.Thread(target=self.send_message, daemon=True).start()

    def send_message(self) -> None:
        self.toggle_progress_bar(True)
        self.send_button.configure(state="disabled")
        user_input = self.message_input.get("1.0", tk.END)
        self.update_chat_display(f"You: {user_input.strip()}")
        self.message_input.delete("1.0", tk.END)
        try:
            chat_response = self.backend.get_chat_response(user_input)
            self.update_chat_display(f"LM: {chat_response}")
        except Exception as e:
            self.update_chat_display(f"Error: {e}")
        self.send_button.configure(state="normal")
        self.toggle_progress_bar(False)

    def update_chat_display(self, message) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(tk.END)

    def run(self) -> None:
        # Start the application
        self.mainloop()
