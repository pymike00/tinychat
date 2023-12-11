from llms import CohereChat, GPT35Turbo, LLMProtocol 


class Backend:
    def __init__(self, llm: LLMProtocol):
        self.llm = llm

    def get_chat_response(self, user_input):
        return self.llm.get_response(user_input)


if __name__ == "__main__":
    llm = GPT35Turbo()
    try:
        llm.init_client()
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
    else: 
        backend = Backend(llm=llm)
        while True:
            user_input = input("You: ")
            chat_response = backend.get_chat_response(user_input)
            print(chat_response)
