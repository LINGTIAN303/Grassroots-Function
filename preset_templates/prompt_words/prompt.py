from grassroots_function.function_descriptor import FunctionDescriptor
from grassroots_function.model_interaction import ModelInteraction
from grassroots_function.api_connector import APIConnector
from roles import get_role_info  # 导入你刚才定义的函数
import json

# 创建类的实例
mi = ModelInteraction("")
fd = FunctionDescriptor()
ac = APIConnector("https://api.openai.com/v1/chat/completions")

# 添加函数描述
fd.add_function(
    name="get_role_info",
    description="获取角色的描述和标签",
    parameters={
        "role_title": {
            "type": "string",
            "description": "角色的标题"
        }
    },
    required=["role_title"]
)

# 调用模型
user_input = "我想了解数据库专家的角色信息"
response = mi.call_model(user_input, fd.get_functions())

# 处理模型的响应
function_call = mi.handle_response(response)

# 打印 function_call 的值
print(function_call)
# 解析 arguments 字符串为字典

arguments = json.loads(function_call['arguments'])
# 检查function_call是否是一个字典

if isinstance(function_call, dict):
    # 调用你的函数
    role_info = get_role_info(arguments['role_title'])

    # 打印 role_info 的值
    print(role_info)

    # 将函数的结果发送回模型
    summarize_response = mi.send_back_result(user_input, role_info, fd.get_functions())

    # 打印 summarize_response 的值
    print(summarize_response)

    # 提取模型的最终消息
    final_message = mi.summarize_response(summarize_response)
    print(final_message)
else:
    print("模型未请求调用任何函数。")
