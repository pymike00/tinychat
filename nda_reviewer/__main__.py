import customtkinter

from nda_reviewer.backend import Backend
from nda_reviewer.ui.chat import ChatApp

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("light")


if __name__ == "__main__":
    backend = Backend()
    nda_reviewer = ChatApp(backend=backend)
    nda_reviewer.run()
