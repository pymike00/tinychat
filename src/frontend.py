import threading
import tkinter as tk

import customtkinter as ctk

from settings import MAIN_WINDOW_RESOLUTION, MAIN_WINDOW_TITLE


class Frontend:
    def __init__(self, backend) -> None:
        # Initialize the backend object
        self.backend = backend

        # Initialize the main window
        self.app = ctk.CTk()
        self.app.title(MAIN_WINDOW_TITLE)
        self.app.geometry(MAIN_WINDOW_RESOLUTION)

        # Create model selection menu
        self.model_selection_menu = ctk.CTkOptionMenu(
            self.app,
            values=self.backend.available_models(),
            command=self.on_model_selection,
        )
        self.model_selection_menu.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")

        # Create a progress bar to enable when getting data from the lms
        self.progress_bar = ctk.CTkProgressBar(self.app, height=10)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.progress_bar.set(1.0)

        # Create a big text area for displaying chat
        self.chat_display = ctk.CTkTextbox(self.app, state="disabled")
        self.chat_display.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        # Create a smaller text area for typing messages
        self.message_input = ctk.CTkTextbox(self.app, height=150)
        self.message_input.grid(row=3, column=0, padx=20, pady=(0, 0), sticky="ew")

        # Create a button for sending messages
        self.send_button = ctk.CTkButton(
            self.app, height=40, text="Send Message to the LM", command=self.on_send_button
        )
        self.send_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.app.after(100, lambda: self.message_input.focus_set())

        # Configure the grid layout
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        # Bind Enter key press to send_message action
        self.app.bind("<Return>", self.on_enter)

        # Bind (CTRL or Shift) + Return to do nothing, so we can use to add space
        self.app.bind("<Control-Return>", self.on_control_enter)
        self.app.bind("<Shift-Return>", self.on_control_enter)

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
        self.app.mainloop()
