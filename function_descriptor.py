import inspect
import functools
import importlib.util

openai_functions = []

type_mapping = {
    "int": "integer",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "list": "array",
    "tuple": "array",
    "dict": "object",
    "None": "null",
}


class FunctionDescriptor:
    def __init__(self):
        self.functions = []

    def add_function(self, name: str, description: str, parameters: dict, required: list) -> None:
        """
        将函数添加到函数列表中。
    
        Args:
            name (str): 函数的名称。
            description (str): 函数的说明。
            parameters (dict): 表示函数参数的字典。
            required (list): 所需参数名称的列表。
        
        Returns:
            None
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


def get_type_mapping(param_type):
    """
    返回给定参数类型的相应类型映射。

    Args:
        param_type (str): 参数类型。

    Returns:
        str: 相应的类型映射。

    """
    # 从参数类型中删除不必要的部分
    param_type = param_type.replace("<class '", '')
    param_type = param_type.replace("'>", '')

    # 返回参数类型的相应类型映射
    return type_mapping.get(param_type, "string")


def get_params_dict(params):
    """
    根据输入参数生成参数详细信息字典。

    Args:
        params (dict): 参数字典。

    Returns:
        dict: 包含参数详细信息的字典。
    """
    params_dict = {}
    # 检查是否安装了 pydantic
    pydantic_found = importlib.util.find_spec("pydantic")
    if pydantic_found:
        from pydantic import BaseModel

    # 迭代输入参数
    for k, v in params.items():
        # 如果安装了 pydantic 并且参数是基本模型的子类
        if pydantic_found and issubclass(v.annotation, BaseModel):
            # 根据 pydantic 架构生成参数详细信息
            params_dict[k] = {
                "type": "object",
                "properties": {
                    field_name: {
                        "type": property.get("type", "unknown"),
                        "description": property.get("description", ""),
                    }
                    for field_name, property in v.annotation.schema()["properties"].items()
                },
            }
        else:
            # 从注释中解析参数类型
            annotation = str(v.annotation).split("[")
            try:
                param_type = annotation[0]
            except IndexError:
                param_type = "string"

            try:
                array_type = annotation[1].strip("]")
            except IndexError:
                array_type = "string"

            # 将参数类型映射到相应的 OpenAPI 类型
            param_type = get_type_mapping(param_type)

            # 生成参数详细信息
            params_dict[k] = {
                "type": param_type,
                "description": "",
            }

            if param_type == "array":
                if "," in array_type:
                    # 处理数组中的多种类型
                    array_types = array_type.split(", ")
                    params_dict[k]["prefixItems"] = []
                    for i, array_type in enumerate(array_types):
                        array_type = get_type_mapping(array_type)
                        params_dict[k]["prefixItems"].append({
                            "type": array_type,
                        })
                else:
                    # 处理数组中的单个类型
                    array_type = get_type_mapping(array_type)
                    params_dict[k]["items"] = {
                        "type": array_type,
                    }

    return params_dict


def oa(func):
    """
    将有关函数的元数据添加到列表的修饰器。
    
    Args:
        func: 要修饰的功能。
    
    Returns:
        装饰功能。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        调用原始函数的包装器函数。
        
        Args:
            *args: 传递给函数的位置参数。
            **kwargs: 传递给函数的关键字参数。
        
        Returns:
            原始函数的返回值。
        """
        return func(*args, **kwargs)

    params = inspect.signature(func).parameters
    param_dict = get_params_dict(params)

    openai_functions.append(
        {
            "name": func.__name__,
            "description": inspect.cleandoc(func.__doc__ or ""),
            "parameters": {
                "type": "object",
                "properties": param_dict,
                "required": list(param_dict.keys()),
            },
        }
    )

    return wrapper


def get_openai_funcs():
    """
    返回 openai 函数的列表。
    """
    return openai_functions
