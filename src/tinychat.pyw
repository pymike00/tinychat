from backend import Backend
from frontend import Frontend


if __name__ == "__main__":
    backend = Backend()
    tinychat = Frontend(backend=backend)
    tinychat.run()
