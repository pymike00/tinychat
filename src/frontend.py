import threading
import tkinter as tk
import customtkinter as ctk


class ChatApp:
    def __init__(self, backend) -> None:
        # Initialize the main window
        self.app = ctk.CTk()
        self.app.title("TinyChat LLM Client")
        self.app.geometry("1200x700")  # Full screen
        self.backend = backend
        # self.app.state('zoomed')  # For full screen on Windows

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.app, values=self.backend.available_models(),
            command=self.backend.set_model
        )
        self.appearance_mode_optionemenu.pack(padx=20, pady=(10, 0))

        # Create a big text area for displaying chat
        self.chat_display = ctk.CTkTextbox(self.app, width=100, state="disabled")
        self.chat_display.pack(expand=True, fill="both", padx=20, pady=(10, 10))

        # Create a smaller text area for typing messages
        self.message_input = ctk.CTkTextbox(self.app, height=150, width=100)
        self.message_input.pack(expand=False, fill="x", padx=20, pady=(0, 0))

        # Create a button for sending messages
        self.send_button = ctk.CTkButton(
            self.app, text="Send Message to the LM", command=self.send_message_thread
        )
        self.send_button.pack(expand=False, fill="x", padx=20, pady=(10, 10))
        self.app.after(100, lambda: self.message_input.focus_set())

    def send_message_thread(self) -> None:
        threading.Thread(target=self.send_message, daemon=True).start()

    def send_message(self) -> None:
        user_input = self.message_input.get("1.0", tk.END)
        self.update_chat_display(f"You: {user_input}")
        self.message_input.delete("1.0", tk.END)
        try:
            chat_response = self.backend.get_chat_response(user_input)
            self.update_chat_display(f"LM: {chat_response}")
        except Exception as e:
            self.update_chat_display(f"Error: {e}")

    def update_chat_display(self, message) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview(tk.END)

    def run(self) -> None:
        # Start the application
        self.app.mainloop()

