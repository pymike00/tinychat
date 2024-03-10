import os
import threading
import tkinter as tk
from tkinter import PhotoImage

import customtkinter as ctk

from tinychat.settings import FONT_FAMILY, MAIN_WINDOW_RESOLUTION, MAIN_WINDOW_TITLE
from tinychat.settings import get_icon_path
from tinychat.ui.frames import SettingsFrame


class ChatApp(ctk.CTk):
    def __init__(self, backend) -> None:
        super().__init__()
        self.set_icon()
        self.model_name = ""

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

        # Create a progress bar to enable when getting data from the LLMs
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=10,
            progress_color="#2c6e49",
        )
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.progress_bar.set(1.0)

        # Create a big text area for displaying chat
        self.chat_display = ctk.CTkTextbox(
            self, state="disabled", font=chat_font, wrap="word", border_spacing=5
        )
        self.chat_display.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Create a smaller text area for typing messages
        self.message_input = ctk.CTkTextbox(
            self, font=chat_font, wrap="word", border_spacing=5
        )
        self.message_input.grid(row=3, column=0, padx=20, pady=(0, 0), sticky="nsew")

        # Create a button for sending messages
        self.send_button = ctk.CTkButton(
            self,
            height=40,
            text="Get Response",
            command=self.on_send_button,
            font=ctk.CTkFont(family=FONT_FAMILY, size=17),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.send_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

        # Set focus (cursor) to message_input automatically
        self.after(100, lambda: self.message_input.focus_set())

        # Configure the grid layout
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bind Enter key press to send_message action
        self.bind("<Return>", self.on_enter)

        # Bind (CTRL or Shift) + Return to do nothing, so we can use to add space
        self.bind("<Control-Return>", self.on_control_enter)
        self.bind("<Shift-Return>", self.on_control_enter)

    def set_icon(self):
        if os.name == "nt":
            self.iconbitmap(default=get_icon_path())
        else:
            # TODO: check if it works on Mac OS
            self.call("wm", "iconphoto", self._w, PhotoImage(file=get_icon_path()))

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
        threading.Thread(target=self.get_response, daemon=True).start()

    def get_response(self) -> None:
        self.toggle_progress_bar(True)
        self.send_button.configure(state="disabled")
        user_input = self.message_input.get("1.0", tk.END)
        self.update_chat_display(f"You: {user_input.strip()}")
        self.message_input.delete("1.0", tk.END)
        try:
            stream_generator = self.backend.get_stream_response(user_input)
            self.update_chat_display(f"\n\n\nLLM: ")
            for data in stream_generator:
                self.update_chat_display(data)
        except Exception as e:
            self.update_chat_display(f"\n\nError: {e}")
        self.update_chat_display("\n\n\n")
        self.send_button.configure(state="normal")
        self.toggle_progress_bar(False)

    def update_chat_display(self, message) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, f"{message}")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(tk.END)

    def run(self) -> None:
        # start w/ fullscreen https://github.com/TomSchimansky/CustomTkinter/discussions/1500
        self._state_before_windows_set_titlebar_color = "zoomed"

        # Start the application
        self.mainloop()
