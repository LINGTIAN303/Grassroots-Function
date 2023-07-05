from model_interaction import ModelInteraction
from function_descriptor import FunctionDescriptor, oa, get_openai_funcs
from api_connector import APIConnector
import os


# 此处定义自定义函数
@oa
def get_current_weather(location: str, country: str) -> str:
    if country == "FR":
        return "The weather is terrible, as always"
    elif location == "California":
        return "The weather is nice and sunny"
    else:
        return "It's rainy and windy"


@oa
def recommend_youtube_channel() -> str:
    return "Unconventional Coding"


@oa
def calculate_str_length(string: str) -> str:
    return str(len(string))


# 初始化类
api_key = os.getenv("OPENAI_API_KEY")
model_interaction = ModelInteraction(api_key)
function_descriptor = FunctionDescriptor()
api_connector = APIConnector("https://api.example.com/")

# 运行对话
prompt = input("You: ")
messages = [{"role": "user", "content": prompt}]
while True:
    response = model_interaction.call_model(prompt, get_openai_funcs())
    function_call = model_interaction.handle_response(response)
    if function_call:
        function_name = function_call["name"]
        arguments = function_call["arguments"]
        function_result = globals()[function_name](**arguments)
        response = model_interaction.send_back_result(prompt, function_result, get_openai_funcs())
    message = model_interaction.summarize_response(response)
    print("ChatGPT: " + message)
    prompt = input("You: ")
