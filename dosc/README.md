# OpenAI Function Caller

OpenAI Function Caller 是一个 Python 包，用于简化使用 OpenAI API 中的 GPT-3.5-turbo-0613 模型的函数调用功能。它提供了一个易于使用的接口，可以轻松地向模型描述函数，让模型智能地选择输出包含调用这些函数的参数的 JSON 对象。

## 安装

使用 pip 安装：

```bash
pip install grassroots-function
```

## 使用

```python
from grassroots_function import ModelInteraction

mi = ModelInteraction("your_openai_api_key")

mi.call_model("What is the weather like in Boston?", [
  {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
])
```

## 贡献

我们欢迎任何形式的贡献！请查看我们的 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详情。

## 许可证

此项目根据 MIT 许可证进行许可 - 请参阅 [LICENSE.md](./LICENSE.md) 文件以获取详情。