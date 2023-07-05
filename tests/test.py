from model_interaction import ModelInteraction
from function_descriptor import FunctionDescriptor, oa, get_openai_funcs
from api_connector import APIConnector
import os
import re

# 初始化类
api_key = os.getenv("OPENAI_API_KEY")
model_interaction = ModelInteraction(api_key)
function_descriptor = FunctionDescriptor()
api_connector = APIConnector("https://api.example.com/")


# 在此处定义自定义函数
@oa
def add_numbers(a: int, b: int):
    """
    将两个数字相加。

    Args:
        a (int): 第一个数字。
        b (int): 第二个数字。

    Returns:
        int: 两个数字的总和。
    """
    
    return a + b



def say_hello(name: str) -> str:
    """
    向名字问好。

    Args:
        name: 要打招呼的名字。

    Returns:
        问候消息。

    Example:
        >>> say_hello("Alice")
        '你好，爱丽丝！'
    """
    return f"Hello, {name}!"


# 测试函数
test_messages = [
    {
        "function": "add_numbers",
        "regex": r'\{\s*"a":\s*42069420,\s*"b":\s*6969420\s*\}',
        "message": {
            "role": "user",
            "content": "What is 42069420 + 6969420?"
        }
    },
    {
        "function": "say_hello",
        "regex": r'\{\s*"name":\s*"OpenAI"\s*\}',
        "message": {
            "role": "user",
            "content": "Say hello to OpenAI"
        }
    },
]

for test in test_messages:
    response = model_interaction.call_model(test["message"]["content"], get_openai_funcs())
    function_call = model_interaction.handle_response(response)
    if not re.search(test["regex"], function_call["arguments"]):
        print("Test failed!")
        break
else:
    print("All tests passed!")
