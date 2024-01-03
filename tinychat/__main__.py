from tinychat.backend import Backend
from tinychat.ui.chat import ChatApp


if __name__ == "__main__":
    backend = Backend()
    tinychat = ChatApp(backend=backend)
    tinychat.run()
