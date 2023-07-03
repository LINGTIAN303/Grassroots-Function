from model_interaction import ModelInteraction
from function_descriptor import FunctionDescriptor
from api_connector import APIConnector

# 初始化类
mi = ModelInteraction("your_api_key")
fd = FunctionDescriptor()
ac = APIConnector("https://api.openai.com/v1/chat/completions")

# 将函数添加到函数列表
fd.add_function(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters={
        "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
        }
    },
    required=["location"]
)

# 使用函数和用户的输入调用模型
user_input = "What is the weather like in Boston?"
response = mi.call_model(user_input, fd.get_functions())

# 从模型的响应中提取函数调用
function_call = mi.handle_response(response)

# 使用函数调用调用第三方 API
api_response = ac.call_api("/weather", "get", function_call['arguments'])

# 将结果发送回模型进行汇总
summarize_response = mi.send_back_result(user_input, api_response, fd.get_functions())

# 从模型的响应中提取最终消息
final_message = mi.summarize_response(summarize_response)

print(final_message)
