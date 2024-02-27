# just a misc file to try some things out

# from llama_cpp import Llama

# # alid formats: ['llama-2', 'alpaca', 'qwen', 'vicuna', 'oasst_llama', 'baichuan-2', 'baichuan',
# # 'openbuddy', 'redpajama-incite', 'snoozy', 'phind', 'intel', 'open-orca', 'mistrallite', 'zephyr',
# # 'pygmalion', 'chatml', 'chatglm3', 'openchat', 'saiga', 'functionary']

# STREAM = True

# llm = Llama(model_path=r"D:\mistral-7b-instruct-v0.2.Q8_0.gguf")#, chat_format="phi2")
# output = llm.create_chat_completion(
#     messages=[
#         # {
#         #     "role": "system",
#         #     "content": "You are a helpful chatbot assistant.",
#         # },
#         {"role": "user", "content": "Hello, who are you?"},
#     ],
#     stream=STREAM
# )

# import json
# if STREAM:
#     for p in output:
#         if "content" in p["choices"][0]["delta"].keys():
#             print(p["choices"][0]["delta"]["content"])
# else:
#     print(output)


from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

chat_handler = Llava15ChatHandler(
    clip_model_path=r"D:\llava_1.5_7B_Q4_K\mmproj-model-f16.gguf"
)
llm = Llama(
    model_path=r"D:\llava_1.5_7B_Q4_K\llava1.5-7b-ggml-model-q4_k.gguf",
    chat_handler=chat_handler,
    n_ctx=2048,  # n_ctx should be increased to accomodate the image embedding
    logits_all=True,  # needed to make llava work
)
stream = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are an assistant who perfectly describes images.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://...-image.png"
                    },
                },
                {"type": "text", "text": "Describe this image very briefly."},
            ],
        },
    ],
    stream=True,
    # temperature=1.0,
)

for piece in stream:
    # print(piece)
    # continue
    if "content" in piece["choices"][0]["delta"].keys():
        print(piece["choices"][0]["delta"]["content"])
