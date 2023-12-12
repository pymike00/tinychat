from backend import Backend
from frontend import ChatApp
from llms import GPT35Turbo # example


if __name__ == "__main__":
    llm = GPT35Turbo()
    backend = Backend(llm=llm)
    tinychat = ChatApp(backend=backend)
    tinychat.run()