import customtkinter as ctk

from tinychat.utils.secrets import get_secret, set_secret
from tinychat.settings import OPENAI_API_KEY_NAME, FONT_FAMILY


class SettingsFrame(ctk.CTkFrame):
    """
    Allows access to api_key settings.
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
        self.grid_columnconfigure(1, weight=1)

        # Create model selection dropdown
        self.model_selection = ctk.CTkOptionMenu(
            self,
            values=available_models,
            command=on_model_select_callback,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            button_color="#1E90FF",
            button_hover_color="#4169E1",
        )
        self.model_selection.grid(
            row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="w"
        )

        # Set default model to OpenAI GPT-4
        default_model = "OpenAI GPT-4"
        if default_model in available_models:
            self.model_selection.set(default_model)

        # Create settings button
        self.settings_button = ctk.CTkButton(
            self,
            text="Settings",
            command=self.open_settings_window,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.settings_button.grid(
            row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="w"
        )

        # Create the new_chat button
        self.reset_button = ctk.CTkButton(
            self,
            text="New Chat",
            command=on_reset_callback,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.reset_button.grid(
            row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="e"
        )

        # Create the export chat button
        self.export_button = ctk.CTkButton(
            self,
            text="Export Conversation",
            command=on_export_callback,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.export_button.grid(
            row=0, column=3, padx=(10, 20), pady=(10, 10), sticky="e"
        )

    def open_settings_window(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("TinyChat - Settings")
        settings_window.geometry("700x360")
        settings_window.transient(self)

        settings_window.grid_columnconfigure(1, weight=1)

        api_key_label = ctk.CTkLabel(settings_window, text="OpenAI API Key: ")
        api_key_label.grid(row=0, column=0, padx=(20, 2), pady=(20, 2), sticky="e")
        self.api_key_entry = ctk.CTkEntry(settings_window)
        self.api_key_entry.insert(0, get_secret(OPENAI_API_KEY_NAME))
        self.api_key_entry.grid(
            row=0, column=1, padx=(2, 20), pady=(20, 2), sticky="ew"
        )

        self.temperature_slider_label = ctk.CTkLabel(
            settings_window, text="Temperature: "
        )
        self.temperature_slider_label.grid(
            row=1, column=0, padx=(20, 2), pady=(10, 2), sticky="w"
        )
        self.temperature_slider = ctk.CTkSlider(
            settings_window,
            from_=0,
            to=10,
            number_of_steps=10,
            command=self.on_temp_slider_event,
        )
        self.temperature_slider.grid(
            row=1, column=1, padx=(20, 2), pady=(10, 2), sticky="ew"
        )
        self.init_temperature_values()

        save = ctk.CTkButton(
            settings_window,
            text="Save Settings",
            command=self.save_settings,
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        save.grid(
            row=2, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky="ew"
        )

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
        set_secret(OPENAI_API_KEY_NAME, self.api_key_entry.get())
        set_secret("temperature", self.temperature_slider.get() / 10)


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
        self.nda_frame.grid(
            row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew"
        )

        # Upload NDA button
        self.upload_nda_button = ctk.CTkButton(
            self.nda_frame, text="Upload NDA", command=self.upload_nda
        )
        self.upload_nda_button.grid(row=0, column=0, padx=5, pady=10)

        # Upload Guidelines button
        self.upload_guidelines_button = ctk.CTkButton(
            self.nda_frame, text="Upload Guidelines", command=self.upload_guidelines
        )
        self.upload_guidelines_button.grid(row=0, column=1, padx=5, pady=10)

        # Analyze and Revise NDA button
        self.analyze_button = ctk.CTkButton(
            self.nda_frame,
            text="Analyze and Revise NDA",
            command=self.analyze_and_revise_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            fg_color=("#0C955A", "#106A43"),
            hover_color="#2c6e49",
        )
        self.analyze_button.grid(row=0, column=2, padx=5, pady=10)

        # Download Revised NDA button
        self.download_nda_button = ctk.CTkButton(
            self.nda_frame,
            text="Download Revised NDA",
            command=self.download_revised_nda,
        )
        self.download_nda_button.grid(row=0, column=3, padx=5, pady=10)

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

    def on_model_selection(self, model_name):
        self.backend.set_model(model_name)
        self.clear_chat()

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", ctk.END)
        self.chat_display.configure(state="disabled")
        self.message_input.delete("0", ctk.END)

    def analyze_and_revise_nda(self):
        try:
            result = self.backend.analyze_and_revise_nda()
            if result == "Analysis complete. Ready to review changes.":
                self.review_changes()
            else:
                messagebox.showinfo("Analyze and Revise NDA", result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def review_changes(self):
        approved_changes = []
        for change in self.backend.review_changes():
            response = messagebox.askyesno(
                "Review Change",
                f"Original: {change['original_text']}\n\nSuggested: {change['suggested_change']}\n\nAccept this change?",
            )
            if response:
                approved_changes.append(change)

        result = self.backend.apply_approved_changes(approved_changes)
        messagebox.showinfo("Changes Applied", result)
