import json


class FunctionDescriptor:
    def __init__(self):
        self.functions = []

    def add_function(self, name, description, parameters, required):
        """将函数添加到函数列表.
    
        Args:
            name (str): 函数的名称。
            description (str): 函数的简要说明。
            parameters (dict): 函数参数的字典。
            required (list): 所需参数的列表。
        """
        function = {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required
            }
        }
        self.functions.append(function)

    def get_functions(self):
        """
        获取函数列表。

        Returns:
            list: 函数列表。
        """
        return self.functions
