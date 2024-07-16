import customtkinter

from tinychat.backend import Backend
from tinychat.ui.chat import ChatApp

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("light")


if __name__ == "__main__":
    backend = Backend()
    tinychat = ChatApp(backend=backend)
    tinychat.run()
