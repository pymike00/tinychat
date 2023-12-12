from backend import Backend
from frontend import ChatApp


if __name__ == "__main__":
    backend = Backend()
    tinychat = ChatApp(backend=backend)
    tinychat.run()