import os
import threading
import tkinter as tk
from tkinter import messagebox
import difflib
from tkinter import ttk
import customtkinter as ctk

from nda_reviewer.settings import FONT_FAMILY, MAIN_WINDOW_RESOLUTION, MAIN_WINDOW_TITLE
from nda_reviewer.ui.frames import SettingsFrame
from nda_reviewer.utils.icon_loader import load_svg_icon


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

        # Load icons
        self.upload_icon = load_svg_icon("upload", color="#FFFFFF")
        self.edit_icon = load_svg_icon("edit-3", color="#FFFFFF")
        self.download_icon = load_svg_icon("download", color="#FFFFFF")
        self.send_icon = load_svg_icon("send", color="#FFFFFF")
        self.settings_icon = load_svg_icon("settings", color="#FFFFFF")
        self.new_chat_icon = load_svg_icon("plus-circle", color="#FFFFFF")

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
            image=self.upload_icon,
            compound="left",
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
            image=self.upload_icon,
            compound="left",
            command=self.upload_guidelines,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.upload_guidelines_button.grid(row=0, column=1, padx=5, pady=10)

        # Revise NDA button
        self.analyze_button = ctk.CTkButton(
            self.bottom_frame,
            text="Revise NDA",
            image=self.edit_icon,
            compound="left",
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
            image=self.download_icon,
            compound="left",
            command=self.download_revised_nda,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
        )
        self.download_nda_button.grid(row=0, column=3, padx=5, pady=10)

        # Create a button for sending messages
        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="",
            image=self.send_icon,
            command=self.send_message_thread,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#1E90FF",
            hover_color="#4169E1",
            width=30,
            height=30,
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

        # Configure styles for ttk widgets
        style = ttk.Style()
        style.configure("TButton", font=(FONT_FAMILY, 12))
        style.configure("TFrame", background="white")

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
            self.update_chat_display(message=f"You: {user_message}\n")
            self.message_input.delete("1.0", tk.END)
            self.send_button.configure(state="disabled")

            try:
                response = self.backend.send_message(user_message)
                self.update_chat_display(message=f"\nAssistant: {response}\n")
            except Exception as e:
                self.update_chat_display(message=f"\nError: {str(e)}\n")
            finally:
                self.send_button.configure(state="normal")

    def update_chat_display(self, message: str) -> None:
        self.chat_display.configure(state="normal")
        if message.startswith("\n"):
            message = message[1:]
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
            if "successfully" in result:
                self.upload_nda_button.configure(
                    fg_color="#28A745", hover_color="#218838"
                )
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def upload_guidelines(self):
        try:
            result = self.backend.upload_guidelines()
            tk.messagebox.showinfo("Upload Guidelines", result)
            if "successfully" in result:
                self.upload_guidelines_button.configure(
                    fg_color="#28A745", hover_color="#218838"
                )
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
            dialog = self.create_change_review_dialog(change)
            if dialog.result:
                approved_changes.append(change)

        result = self.backend.apply_approved_changes(approved_changes)
        tk.messagebox.showinfo("Changes Applied", result)

    def create_change_review_dialog(self, change):
        dialog = tk.Toplevel(self)
        dialog.title(f"Review Change")
        dialog.geometry("1000x600")
        dialog.transient(self)  # Make dialog transient of main window
        dialog.grab_set()  # Make dialog modal
        dialog.overrideredirect(True)  # Remove decorations
        dialog.geometry(
            "+%d+%d" % (self.winfo_x() + 100, self.winfo_y() + 100)
        )  # Set fixed position

        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Original text
        original_label = ttk.Label(
            frame, text="Original Text:", font=(FONT_FAMILY, 12, "bold")
        )
        original_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        original_text = tk.Text(frame, wrap=tk.WORD, width=60, height=8)
        original_text.grid(row=1, column=0, padx=(0, 5), sticky="nsew")
        original_text.insert(tk.END, change["original_text"])
        original_text.config(state=tk.DISABLED)

        # Suggested change
        suggested_label = ttk.Label(
            frame, text="Suggested Change:", font=(FONT_FAMILY, 12, "bold")
        )
        suggested_label.grid(row=0, column=1, sticky="w", pady=(0, 5))
        suggested_text = tk.Text(frame, wrap=tk.WORD, width=60, height=8)
        suggested_text.grid(row=1, column=1, padx=(5, 0), sticky="nsew")
        self.insert_with_track_changes(
            suggested_text, change["original_text"], change["suggested_change"]
        )
        suggested_text.config(state=tk.DISABLED)

        # Justification
        justification_label = ttk.Label(
            frame, text="Justification:", font=(FONT_FAMILY, 12, "bold")
        )
        justification_label.grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(10, 5)
        )
        justification_text = tk.Text(frame, wrap=tk.WORD, width=120, height=6)
        justification_text.grid(row=3, column=0, columnspan=2, sticky="nsew")
        justification_text.insert(tk.END, change["justification"])
        justification_text.config(state=tk.DISABLED)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        accept_button = ttk.Button(
            button_frame, text="Accept", command=lambda: self.close_dialog(dialog, True)
        )
        accept_button.pack(side=tk.LEFT, padx=(0, 5))

        reject_button = ttk.Button(
            button_frame,
            text="Reject",
            command=lambda: self.close_dialog(dialog, False),
        )
        reject_button.pack(side=tk.LEFT)

        dialog.result = None
        dialog.wait_window()

        return dialog

    def insert_with_track_changes(self, text_widget, original, suggested):
        differ = difflib.Differ()
        diff = list(differ.compare(original.split(), suggested.split()))

        for word in diff:
            if word.startswith("  "):
                text_widget.insert(tk.END, word[2:] + " ")
            elif word.startswith("- "):
                text_widget.insert(tk.END, word[2:] + " ", "deleted")
            elif word.startswith("+ "):
                text_widget.insert(tk.END, word[2:] + " ", "added")

        text_widget.tag_configure("deleted", foreground="red", overstrike=True)
        text_widget.tag_configure("added", foreground="green", underline=True)

    def close_dialog(self, dialog, result):
        dialog.result = result
        dialog.destroy()

    def set_initial_model(self):
        initial_model = self.settings_frame.model_selection.get()
        self.model_name = initial_model
        self.backend.set_model(model_name=initial_model)
