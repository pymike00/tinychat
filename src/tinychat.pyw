from backend import Backend
from ui.chat import ChatApp


if __name__ == "__main__":
    backend = Backend()
    tinychat = ChatApp(backend=backend)
    tinychat.run()
