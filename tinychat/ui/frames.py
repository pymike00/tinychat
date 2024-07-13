import customtkinter as ctk

from tinychat.utils.secrets import get_secret, set_secret
from tinychat.settings import OPENAI_API_KEY_NAME, OPENAI_ASSISTANT_ID


class SettingsFrame(ctk.CTkFrame):
    """
    Allows model selection and access to api_key settings.
    """

    def __init__(
        self,
        parent,
        available_models,
        on_model_select_callback,
        on_reset_callback,
        on_export_callback,
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        self.grid_columnconfigure(2, weight=1)

        # Create model selection menu
        self.model_selection_menu = ctk.CTkOptionMenu(
            self,
            values=available_models,
            command=on_model_select_callback,
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            dropdown_font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            fg_color=("#0C955A", "#106A43"),
        )
        self.model_selection_menu.grid(
            row=0, column=0, padx=(20, 0), pady=(10, 5), sticky="w"
        )

        # Create settings button
        self.settings_button = ctk.CTkButton(
            self,
            text="Settings",
            command=self.open_settings_window,
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.settings_button.grid(
            row=0, column=1, padx=(10, 20), pady=(10, 5), sticky="e"
        )

        # Create the new_chat button
        self.reset_button = ctk.CTkButton(
            self,
            text="New Chat",
            command=on_reset_callback,
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.reset_button.grid(row=0, column=2, padx=(10, 0), pady=(10, 5), sticky="e")

        # Create the export chat button
        self.export_button = ctk.CTkButton(
            self,
            text="Export Conversation",
            command=on_export_callback,
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.export_button.grid(
            row=0, column=3, padx=(10, 20), pady=(10, 5), sticky="e"
        )

    def open_settings_window(self):
        """
        Open settings window where API keys can be configured.
        """
        # TODO: fix layout and refactor

        # Create a new top-level window for settings
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("TinyChat - Settings")
        settings_window.geometry("700x360")  # Adjusted size to fit API key entries
        settings_window.transient(
            self
        )  # type:ignore - Set to be on top of the main window

        # Configure grid layout
        settings_window.grid_columnconfigure(1, weight=1)

        # Add widgets to the settings window for API key entries
        api_key_label_1 = ctk.CTkLabel(settings_window, text="OpenAI API Key: ")
        api_key_label_1.grid(row=0, column=0, padx=(20, 2), pady=(20, 2), sticky="e")
        self.api_key_entry_1 = ctk.CTkEntry(settings_window)
        self.api_key_entry_1.insert(0, get_secret(OPENAI_API_KEY_NAME))
        self.api_key_entry_1.grid(
            row=0, column=1, padx=(2, 20), pady=(20, 2), sticky="ew"
        )

        api_key_label_2 = ctk.CTkLabel(settings_window, text="OpenAI Assistant ID: ")
        api_key_label_2.grid(row=1, column=0, padx=(20, 2), pady=(10, 2), sticky="e")
        self.api_key_entry_2 = ctk.CTkEntry(settings_window)
        self.api_key_entry_2.insert(0, get_secret(OPENAI_ASSISTANT_ID))
        self.api_key_entry_2.grid(
            row=1, column=1, padx=(2, 20), pady=(10, 2), sticky="ew"
        )

        self.temperature_slider_label = ctk.CTkLabel(
            settings_window, text="Temperature: "
        )
        self.temperature_slider_label.grid(
            row=6, column=0, padx=(20, 2), pady=(10, 2), sticky="w"
        )
        self.temperature_slider = ctk.CTkSlider(
            settings_window,
            from_=0,
            to=10,
            number_of_steps=10,
            command=self.on_temp_slider_event,
        )
        self.temperature_slider.grid(
            row=6, column=1, padx=(20, 2), pady=(10, 2), sticky="w"
        )
        self.init_temperature_values()

        self.status_label = ctk.CTkLabel(settings_window, text="")
        self.status_label.grid(row=7, column=0, padx=(20, 2), pady=(0, 2), sticky="w")

        # Add a close button to the settings window
        close = ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        close.grid(row=8, column=1, padx=(0, 0), pady=(0, 0), sticky="w")

        # Add a save button to the settings window
        save = ctk.CTkButton(
            settings_window,
            text="Save Settings",
            command=self.save_settings,
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        save.grid(row=8, column=1, padx=(150, 0), pady=(0, 0), sticky="w")

    def init_temperature_values(self):
        temperature = get_secret("temperature")
        if not temperature:
            temperature = 0.0
        self.temperature_slider_label.configure(text=f"Temperature: {str(temperature)}")
        self.temperature_slider.set(temperature * 10)

    def on_temp_slider_event(self, value):
        """Update the temperature_slider_label.

        TODO: currently you must restart the app if temperature is changed.
        Update the code so that the backend send temperature to update the backend
        and the llm handler.
        """
        temperature = value / 10
        self.temperature_slider_label.configure(text=f"Temperature: {str(temperature)}")

    def save_settings(self):
        set_secret(OPENAI_API_KEY_NAME, self.api_key_entry_1.get())
        set_secret(OPENAI_ASSISTANT_ID, self.api_key_entry_2.get())
        set_secret("temperature", self.temperature_slider.get() / 10)
        self.status_label.configure(text="Saved.")

from tkinter import messagebox

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, backend):
        super().__init__(master)
        self.backend = backend
        self.create_widgets()

    def create_widgets(self):
        # ... (existing widgets)

        # Add a new frame for NDA-related buttons
        self.nda_frame = ctk.CTkFrame(self)
        self.nda_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Upload NDA button
        self.upload_nda_button = ctk.CTkButton(self.nda_frame, text="Upload NDA", command=self.upload_nda)
        self.upload_nda_button.grid(row=0, column=0, padx=5, pady=5)

        # Upload Guidelines button
        self.upload_guidelines_button = ctk.CTkButton(self.nda_frame, text="Upload Guidelines", command=self.upload_guidelines)
        self.upload_guidelines_button.grid(row=0, column=1, padx=5, pady=5)

        # Download Revised NDA button
        self.download_nda_button = ctk.CTkButton(self.nda_frame, text="Download Revised NDA", command=self.download_revised_nda)
        self.download_nda_button.grid(row=0, column=2, padx=5, pady=5)

    def upload_nda(self):
        try:
            result = self.backend.upload_nda()
            messagebox.showinfo("Upload NDA", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def upload_guidelines(self):
        try:
            result = self.backend.upload_guidelines()
            messagebox.showinfo("Upload Guidelines", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def download_revised_nda(self):
        try:
            result = self.backend.download_revised_nda()
            messagebox.showinfo("Download Revised NDA", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ... (other existing methods)