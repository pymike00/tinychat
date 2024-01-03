import customtkinter as ctk

from api_keys import get_api_key, set_api_key
from settings import (
    COHERE_API_KEY_NAME,
    OPENAI_API_KEY_NAME,
    MISTRAL_API_KEY_NAME,
    FONT_FAMILY,
)


class SettingsFrame(ctk.CTkFrame):
    """
    Allows model selection and access to api_key settings.
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
            dropdown_font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
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
        """
        Open settings window where API keys can be configured.
        """
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
        self.api_key_entry_1.insert(0, get_api_key(OPENAI_API_KEY_NAME))
        self.api_key_entry_1.grid(
            row=0, column=1, padx=(2, 20), pady=(20, 2), sticky="ew"
        )

        api_key_label_2 = ctk.CTkLabel(settings_window, text="Mistral API Key: ")
        api_key_label_2.grid(row=1, column=0, padx=(20, 2), pady=(10, 2), sticky="e")
        self.api_key_entry_2 = ctk.CTkEntry(settings_window)
        self.api_key_entry_2.insert(0, get_api_key(MISTRAL_API_KEY_NAME))
        self.api_key_entry_2.grid(
            row=1, column=1, padx=(2, 20), pady=(10, 2), sticky="ew"
        )

        api_key_label_3 = ctk.CTkLabel(settings_window, text="Cohere API Key: ")
        api_key_label_3.grid(row=2, column=0, padx=(20, 2), pady=(10, 2), sticky="e")
        self.api_key_entry_3 = ctk.CTkEntry(settings_window)
        self.api_key_entry_3.insert(0, get_api_key(COHERE_API_KEY_NAME))
        self.api_key_entry_3.grid(
            row=2, column=1, padx=(2, 20), pady=(10, 2), sticky="ew"
        )

        self.status_label = ctk.CTkLabel(settings_window, text="")
        self.status_label.grid(row=3, column=0, padx=(20, 2), pady=(10, 2), sticky="w")

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
        set_api_key(OPENAI_API_KEY_NAME, self.api_key_entry_1.get())
        set_api_key(MISTRAL_API_KEY_NAME, self.api_key_entry_2.get())
        set_api_key(COHERE_API_KEY_NAME, self.api_key_entry_3.get())
        self.status_label.configure(text="Saved.")
