import openai
import json


class ModelInteraction:
    def __init__(self, api_key):
        openai.api_key = api_key

    def call_model(self, user_input, functions):
        """
        使用函数和用户的输入调用模型
    
        Args:
            user_input (str): 用户的输入
            functions (list): 要传递给模型的函数列表
    
        Returns:
            response (object): 模型返回的响应对象，如果发生错误，则返回 None（如果发生错误）
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[{"role": "user", "content": user_input}],
                functions=functions
            )
            return response
        except Exception as e:
            print(f"Error in calling the model: {e}")
            return None

    def handle_response(self, response):
        """从模型的响应中提取函数调用。"""
    
        # 检查响应是否不是“None”
        if response is not None:
            # 从响应中获取选项
            choices = response['choices']
        
            # 检查是否存在选项
            if choices:
                # 从首选中获得function_call
                function_call = choices[0]['message']['function_call']
                return function_call
            else:
                # 如果未找到函数调用，则打印错误消息
                print("No function call found in model's response")
                return None
        else:
            # 如果未收到响应，则打印错误消息
            print("No response received from the model")
            return None

    def send_back_result(self, user_input, function_result, functions):
        """
        将结果发送回模型进行汇总。

        Args:
            user_input (str): 要包含在对话中的用户输入。
            function_result (str): 要包含在会话中的函数调用的结果。
            functions (list): 模型要使用的函数列表。

        Returns:
            response: 来自模型的响应。
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": None, "function_call": function_result}
                ],
                functions=functions
            )
            return response
        except Exception as e:
            print(f"Error in sending back the result: {e}")
            return None

    def summarize_response(self, response):
        """从模型的响应中提取最终消息。
    
        Args:
            response (dict): 来自模型的响应对象。
        
        Returns:
            str: 从响应中提取的最后一条消息，如果未找到消息，则为 None 。
        """
        # 检查响应是否不是“None”
        if response is not None:
            choices = response['choices']
            # 检查响应中是否存在选项
            if choices:
                message = choices[0]['message']['content']
                return message
            else:
                # 如果未找到最终消息，则打印错误消息
                print("No final message found in model's response")
                return None
        else:
            # 如果未收到响应，则打印错误消息
            print("No response received from the model")
            return None
