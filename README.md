<!-- TOC -->
* # 文档目录
- [Grassroots Function](#grassroots-function)
    - [1. 对项目有什么帮助？](#对项目有什么帮助)
    - [2. 项目中我需要做什么？](#项目中我需要做什么)
    - [3. 两个假设的项目中使用这个包时的编写示例](#两个假设的项目中使用这个包时的编写示例)
        - [3.1. 第一个示例](#第一个示例)
        - [3.2. 第二个示例](#第二个示例)
    - [4. 安装](#安装)
    - [5. 使用](#使用)
    - [6. 详细的使用方法](#详细的使用方法)
        - [6.1. **安装包**](#1-安装包)
        - [6.2. **导入类**](#2-导入类)
        - [6.3. **创建类的实例**](#3-创建类的实例)
        - [6.4. **添加函数描述**](#4-添加函数描述)
        - [6.5. **调用模型**](#5-调用模型)
        - [6.6. **处理模型的响应**](#6-处理模型的响应)
        - [6.7. **调用第三方 API**](#7-调用第三方-api)
        - [6.8. **将 API 的响应发送回模型**](#8-将-api-的响应发送回模型)
        - [6.9. **提取模型的最终消息**](#9-提取模型的最终消息)
    - [7. 贡献](#贡献)
    - [8. 许可](#许可)

<!-- /TOC -->
# Grassroots Function

这是一个 Python 包，用于使用 OpenAI 的 GPT-3.5-turbo-0613 模型来调用函数。你可以使用这个包来创建复杂的对话系统，这些系统可以通过调用外部 API 来回答用户的问题。
***
## 对项目有什么帮助？
这个包在项目中提供了一种新的方式来更可靠地连接 GPT-3.5-turbo-0613 模型的能力和外部工具/API。它使得开发者可以以函数调用的形式获取模型的结构化数据返回，这对于许多应用场景都非常有用，例如：

1. **创建聊天机器人**：使用这个包，你可以创建一个聊天机器人，该机器人能够通过调用外部工具（例如天气查询API，邮件发送API等）来回答问题。

2. **自然语言转API调用**：这个包还可以将自然语言查询转换为 API 调用或数据库查询。例如，可以将 "Who are my top ten customers this month?" 转换为一个内部 API 调用。

3. **提取结构化数据**：此外，这个包还可以从文本中提取结构化数据。例如，可以定义一个函数，从 Wikipedia 文章中提取所有提到的人的数据。

4. **封装和管理函数调用**：这个包也提供了管理函数描述的工具，使得开发者可以随时添加新的函数描述，并且可以根据函数描述的 JSON 架构来调用函数。

5. **连接第三方API**：这个包还封装了一个用于与第三方API进行交互的类，开发者可以使用它来调用任何外部API。

总的来说，这个包极大地扩展了 GPT-3.5-turbo-0613 模型的应用范围，使得它不仅可以用于生成文本，还可以用于执行实际的任务，例如查询数据，发送邮件，获取天气等等。
***
## 项目中我需要做什么？
在导入这个包之后，你需要做的主要工作就是：

1. **添加函数描述**：使用 `FunctionDescriptor` 类的 `add_function` 方法，你可以添加函数描述。这个函数描述应该包括函数名，函数描述，参数类型，以及哪些参数是必需的。

2. **添加外部API的调用方式**：在 `APIConnector` 类中，你需要提供外部API的基本URL，并且需要在调用 `call_api` 方法时提供正确的API路径、请求类型（如"get"、"post"等）以及请求参数。

3. **调用模型并处理响应**：使用 `ModelInteraction` 类，你可以调用模型，处理模型的响应，调用第三方API，然后将API的响应发送回模型。

这个包的设计目的就是为了简化这个过程，使得你只需要关注你的业务逻辑，而不需要关注如何与GPT-3.5-turbo-0613模型和外部API进行交互。
***
## 两个假设的项目中使用这个包时的编写示例
### 第一个示例
以下是使用这个包的一个基本示例。假设我们正在创建一个聊天机器人，这个机器人可以回答有关天气的问题。

首先，我们需要创建一个天气查询的函数描述。函数的名字是 "get_current_weather"，它有两个参数，一个是 "location"，另一个是 "unit"。

```python
from grassroots_function import FunctionDescriptor

func_desc = FunctionDescriptor()
func_desc.add_function(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Unit of temperature"
            }
        },
        "required": ["location"]
    }
)
```

然后，我们需要创建一个 `APIConnector` 类的实例，这个实例可以用来调用天气查询API。

```python
from grassroots_function import APIConnector

api_connector = APIConnector(base_url="https://weatherapi.com")
```

最后，我们使用 `ModelInteraction` 类来调用模型，并处理模型的响应。

```python
from grassroots_function import ModelInteraction

model_interaction = ModelInteraction(model="gpt-3.5-turbo-0613", func_desc=func_desc, api_connector=api_connector)

# 用户的问题
user_question = "What is the weather like in Boston?"

# 调用模型
model_response = model_interaction.call_model(user_question)

# 如果模型的响应包含函数调用，那么调用相应的API
if model_response.function_call:
    api_response = model_interaction.call_api(
        path="/current_weather", 
        request_type="get", 
        params=model_response.function_call.arguments
    )

    # 将API的响应发送回模型，得到模型的最终回答
    final_answer = model_interaction.process_api_response(api_response)
else:
    final_answer = model_response.content

print(final_answer)
```

以上就是一个使用这个包的基本示例。当然，这个包的使用方法可以根据你的具体需求进行调整。
***
### 第二个示例
如果您想使用 Wolfram Alpha API，可以按照类似的方式进行操作。以下是一个使用 Wolfram Alpha API 的示例。

首先，您需要创建一个函数描述。假设我们创建一个名为 "query_wolfram" 的函数，它只需要一个参数 "question"。

```python
from grassroots_function import FunctionDescriptor

func_desc = FunctionDescriptor()
func_desc.add_function(
    name="query_wolfram",
    description="Query Wolfram Alpha for a given question",
    parameters={
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to ask Wolfram Alpha"
            }
        },
        "required": ["question"]
    }
)
```

然后，我们需要创建一个 `APIConnector` 类的实例，这个实例可以用来调用 Wolfram Alpha API。Wolfram Alpha API 需要一个 App ID，这个 App ID 应该在调用 API 时作为参数传递。

```python
from grassroots_function import APIConnector

api_connector = APIConnector(base_url="http://api.wolframalpha.com/v2")
```

最后，我们使用 `ModelInteraction` 类来调用模型，并处理模型的响应。

```python
from grassroots_function import ModelInteraction

model_interaction = ModelInteraction(model="gpt-3.5-turbo-0613", func_desc=func_desc, api_connector=api_connector)

# 用户的问题
user_question = "What is the derivative of x^2?"

# 调用模型
model_response = model_interaction.call_model(user_question)

# 如果模型的响应包含函数调用，那么调用相应的API
if model_response.function_call:
    api_response = model_interaction.call_api(
        path="/result", 
        request_type="get", 
        params={"input": model_response.function_call.arguments["question"], "appid": "YOUR_WOLFRAM_APP_ID"}
    )

    # 将API的响应发送回模型，得到模型的最终回答
    final_answer = model_interaction.process_api_response(api_response)
else:
    final_answer = model_response.content

print(final_answer)
```

在这个示例中，我们假设 Wolfram Alpha API 的响应是一个可以直接发送给模型的字符串。如果实际的响应是一个复杂的 JSON 对象，那么你可能需要在 `process_api_response` 方法中添加一些代码，来将这个 JSON 对象转换为一个字符串。
***
## 安装

你可以使用 pip 来安装这个包：

```bash
pip install grassroots-function #未发布pypi，请拉取到本地并导航到该包的根目录后使用该命令
```

## 使用

以下是一个基本的使用例子：

```python
from grassroots_function import ModelInteraction, FunctionDescriptor, APIConnector

# Initialize the classes
mi = ModelInteraction("your_openai_api_key")
fd = FunctionDescriptor()
ac = APIConnector("your_base_api_url")

# Add a function to the function list
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

# Call the model with functions and the user's input
user_input = "What is the weather like in Boston?"
response = mi.call_model(user_input, fd.get_functions())

# Extract function call from model's response
function_call = mi.handle_response(response)

# Call the third party API with the function call
api_response = ac.call_api("/weather", "get", function_call['arguments'])

# Send the result back to the model to summarize
summarize_response = mi.send_back_result(user_input, api_response, fd.get_functions())

# Extract the final message from model's response
final_message = mi.summarize_response(summarize_response)

print(final_message)
```

注意：你需要用你自己的 OpenAI API 密钥替换 "your_openai_api_key"，用你自己的 API 基本 URL 替换 "your_base_api_url"，并根据你的实际情况修改函数描述和第三方 API 的调用。
***
## 详细的使用方法
这个包的使用方式大致如下：

### 1. **安装包**

   首先，你需要将这个包安装到你的 Python 环境中。这个包并未发布到 PyPI，你可以拉取这个包后到本地后使用 `pip` 进行安装。进入包的根目录，然后使用 `pip install .` 进行安装。

### 2. **导入类**

   安装完成后，你可以在你的项目中导入这个包中的类：

   ```python
   from grassroots_function import ModelInteraction, FunctionDescriptor, APIConnector
   ```

### 3. **创建类的实例**

   然后，你可以创建这些类的实例：

   ```python
   mi = ModelInteraction("your_openai_api_key")
   fd = FunctionDescriptor()
   ac = APIConnector("your_base_api_url")
   ```

   将 `"your_openai_api_key"` 和 `"your_base_api_url"` 替换为你的 OpenAI API 密钥和你的OpenAI聊天完成的API URL。

### 4. **添加函数描述**

   使用 `FunctionDescriptor` 的 `add_function` 方法，添加函数描述：

   ```python
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
   ```

### 5. **调用模型**

   使用 `ModelInteraction` 的 `call_model` 方法，调用模型：

   ```python
   user_input = "What is the weather like in Boston?"
   response = mi.call_model(user_input, fd.get_functions())
   ```

### 6. **处理模型的响应**

   使用 `ModelInteraction` 的 `handle_response` 方法，处理模型的响应，并提取出模型要调用的函数：

   ```python
   function_call = mi.handle_response(response)
   ```

### 7. **调用第三方 API**

   使用 `APIConnector` 的 `call_api` 方法，调用第三方 API：

   ```python
   api_response = ac.call_api("/weather", "get", function_call['arguments'])
   ```

### 8. **将 API 的响应发送回模型**

   使用 `ModelInteraction` 的 `send_back_result` 方法，将 API 的响应发送回模型：

   ```python
   summarize_response = mi.send_back_result(user_input, api_response, fd.get_functions())
   ```

### 9. **提取模型的最终消息**

   使用 `ModelInteraction` 的 `summarize_response` 方法，提取模型的最终消息：

   ```python
   final_message = mi.summarize_response(summarize_response)
   print(final_message)
   ```
这就是如何使用这个包的基本步骤。如果你有任何疑问，或者需要进一步的帮助，请提交`issue`，我很乐意提供帮助。
***
## 贡献

欢迎任何形式的贡献！如果你有任何问题或者建议，请提交 issue 或者 pull request。

## 许可

这个包遵循 MIT 许可。