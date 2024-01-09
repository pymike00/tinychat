import customtkinter

from tinychat.backend import Backend
from tinychat.ui.chat import ChatApp

customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



if __name__ == "__main__":
    backend = Backend()
    tinychat = ChatApp(backend=backend)
    tinychat.run()
