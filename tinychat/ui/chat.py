import os
import threading
import tkinter as tk
from tkinter import PhotoImage, messagebox

import customtkinter as ctk

from tinychat.settings import FONT_FAMILY, MAIN_WINDOW_RESOLUTION, MAIN_WINDOW_TITLE
from tinychat.settings import get_icon_path
from tinychat.ui.frames import SettingsFrame

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

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

        # Add weather label
        self.weather_label = ctk.CTkLabel(
            self,
            text=self.get_weather(),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
        )
        self.weather_label.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="w")

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
        self.analyze_button = ctk.CTkButton(
            self,
            height=40,
            text="Analyze and Revise NDA",
            command=self.analyze_and_revise_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=17),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.analyze_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

        # Create a frame for NDA-related buttons
        self.nda_frame = ctk.CTkFrame(self)
        self.nda_frame.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="ew")

        # Upload NDA button
        self.upload_nda_button = ctk.CTkButton(
            self.nda_frame,
            text="Upload NDA",
            command=self.upload_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.upload_nda_button.grid(row=0, column=0, padx=5, pady=5)

        # Upload Guidelines button
        self.upload_guidelines_button = ctk.CTkButton(
            self.nda_frame,
            text="Upload Guidelines",
            command=self.upload_guidelines,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.upload_guidelines_button.grid(row=0, column=1, padx=5, pady=5)

        # Download Revised NDA button
        self.download_nda_button = ctk.CTkButton(
            self.nda_frame,
            text="Download Revised NDA",
            command=self.download_revised_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.download_nda_button.grid(row=0, column=2, padx=5, pady=5)

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

        self.update_weather()

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

    def send_message_thread(self) -> None:
        threading.Thread(target=self.get_response, daemon=True).start()

    def get_response(self) -> None:
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
            tk.messagebox.showinfo("Analyze and Revise NDA", result)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def get_weather(self):
        owm = OWM('YOUR_API_KEY')  # Replace with your OpenWeatherMap API key
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place('Boston,US')
        w = observation.weather
        return f"Boston: {w.temperature('celsius')['temp']:.1f}°C, {w.detailed_status}"

    def update_weather(self):
        self.weather_label.configure(text=self.get_weather())
        self.after(600000, self.update_weather)  # Update every 10 minutes