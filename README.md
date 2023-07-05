# Grassroots Function
***
这是一个 Python 包，用于使用 OpenAI API的 `GPT-3.5-turbo-0613` `GPT-4-0613`模型来调用函数。你可以使用这个包来创建复杂的对话系统，这些系统可以通过调用外部 API 来回答用户的问题。
# 文档目录
***
<!-- TOC -->

- [Grassroots Function](#grassroots-function)
    - [1. 对项目有什么帮助？](#对项目有什么帮助)
        - [1.1. 主要优点和增强功能](#主要优点和增强功能)
    - [2. 项目中我需要怎么使用它编写和做什么？](#项目中我需要怎么使用它编写和做什么)
    - [3. 安装](#安装)
    - [4. 使用示例代码](#使用示例代码)
    - [5. 详细的使用方法](#详细的使用方法)
        - [5.1. **安装包**](#1-安装包)
        - [5.2. **导入包**](#2-导入包)
        - [5.3. **初始化类**](#3-初始化类)
        - [5.4. **定义函数**](#4-定义函数)
        - [5.5. **运行对话**](#5-运行对话)
    - [6. 计划实现](#计划实现)
        - [6.1. 预置方向](#预置方向)
        - [6.2. 功能方向](#功能方向)
        - [6.3. 优化方向](#优化方向)
    - [7. 版本](#版本)
    - [8. 贡献](#贡献)
    - [9. 许可](#许可)

<!-- /TOC -->
***
## 对项目有什么帮助？
这个包在项目中提供了一种新的方式来更可靠地连接 GPT-3.5-turbo-0613 模型的能力和外部工具/API。它使得开发者可以以函数调用的形式获取模型的结构化数据返回，这对于许多应用场景都非常有用，例如：
### 主要优点和增强功能
新项目的主要优点和增强功能包括：

1. **自动函数定义**：通过`@oa`装饰器，你可以更容易地定义函数，而不需要手动创建函数的定义。
2. **自动函数管理**：通过`FunctionDescriptor`类，你可以更容易地管理你的函数，包括添加新的函数和获取所有的函数。
3. **自动模型交互**：通过`ModelInteraction`类，你可以更容易地与OpenAI的GPT模型进行交互，包括调用模型、处理模型的响应、将函数调用的结果发送回模型、提取模型的最终消息等。
4. **自动API交互**：通过`APIConnector`类，你可以更容易地与外部API进行交互，包括调用API并获取响应。

_总的来说，这个包极大地扩展了 GPT-3.5-turbo-0613 模型的应用范围，使得它不仅可以用于生成文本，还可以用于执行实际的任务，例如查询数据，发送邮件，获取天气等等。_
***
## 项目中我需要怎么使用它编写和做什么？
在导入这个包之后，你需要做的主要编写工作就是：

1. **初始化类**：看详情请点击[这里](#3-初始化类)

2. **定义函数**：看详情请点击[这里](#4-定义函数)

3. **在`main.py`文件中**：使用`@oa`装饰器定义你的函数。

4. **运行`main.py`文件**：输入你的对话提示，然后程序将自动处理函数调用和模型交互。

_这个包的设计目的就是为了简化这个过程，使得你只需要关注你的业务逻辑，而不需要关注如何与GPT-3.5-turbo-0613模型和外部API进行交互。_
***
## 安装

你可以使用 pip 来安装这个包：

```bash
pip install grassroots-function #未发布pypi，请拉取到本地并导航到该包的根目录后使用该命令
```

## 使用示例代码

以下是一个示例代码：

```python
import grassroots_function

# Initialize the classes
api_key = "your_openai_api_key"
model_interaction = grassroots_function.ModelInteraction(api_key)
function_descriptor = grassroots_function.FunctionDescriptor()

# Define your functions
@grassroots_function.oa
def add_numbers(a: int, b: int):
    return a + b

@grassroots_function.oa
def say_hello(name: str):
    return f"Hello, {name}!"

# Run the conversation
prompt = input("You: ")
response = model_interaction.call_model(prompt, function_descriptor.get_functions())
print(response)
```

_在这个示例代码中，我们首先导入了该包，然后我们初始化了`ModelInteraction`和`FunctionDescriptor`类，定义了一些函数，然后我们运行了一个对话，其中包括调用模型和处理模型的响应。_
***
## 详细的使用方法
这个包的使用方式大致如下：

### 1. **安装包**

   首先，你需要将这个包安装到你的 Python 环境中。这个包并未发布到 PyPI，你可以拉取这个包后到本地后使用 `pip` 进行安装。进入包的根目录，然后使用 `pip install .` 进行安装。

### 2. **导入包**

   安装完成后，你可以在你的项目中导入这个包中的类：

   ```python
   from grassroots_function import ModelInteraction, FunctionDescriptor, APIConnector
   ```

### 3. **初始化类**

   然后，你需要初始化`ModelInteraction`和`FunctionDescriptor`类。你需要提供你的OpenAI API密钥来初始化`ModelInteraction`类。

   ```python
   api_key = "your_openai_api_key"
   model_interaction = grassroots_function.ModelInteraction(api_key)
   function_descriptor = grassroots_function.FunctionDescriptor()
   ```

### 4. **定义函数**

   你可以使用`@oa`装饰器来定义你的函数。这个装饰器会自动创建函数的描述，并添加到`FunctionDescriptor`类中。

   ```python
    @grassroots_function.oa
    def add_numbers(a: int, b: int):
        return a + b

    @grassroots_function.oa
    def say_hello(name: str):
        return f"Hello, {name}!"
```

### 5. **运行对话**

   你可以使用`ModelInteraction`类的`call_model`方法来运行对话。你需要提供你的对话提示和函数描述。

   ```python
    prompt = input("You: ")
    response = model_interaction.call_model(prompt, function_descriptor.get_functions())
    print(response)
   ```
  * 这个方法会自动处理函数调用和模型交互，并返回模型的响应。
  * 你也可以使用`GPT-4-0613`模型，调用openai.ChatCompletion.create方法处写入：
```python
    response = openai.ChatCompletion.create(
    model="gpt-4-0613", #这里
    messages=[{"role": "user", "content": user_input}],
    functions=functions
)
```

_以上就是使用该包的步骤。通过这些步骤，你可以更容易地定义和使用函数，同时也可以更容易地与OpenAI的GPT模型和外部API进行交互。如果你有任何疑问，或者需要进一步的帮助，请提交_`issue`_，我很乐意提供帮助。_
***
## 计划实现
### 预置方向
* 已完成：```🟩``` 无
* 半成品：```🟨``` [提示词]("preset_templates\prompt_words\PROMPT.md")
* 未完成：```◻️``` 搜索 ```◻️``` Stable-Diffusion
### 功能方向
```◻️``` 一个秘密的功能

```◻️```本地数据知识数据库
### 优化方向
```◻️``` 结构性

```◻️``` 一些错误的代码

```◻️``` 更多的项目支持
***
## 版本
💮 [v0.0.5版本信息]("dosc\version\README v0.0.5.md")

💮 [v0.0.1版本信息]("dosc\version\README v0.0.1.md")
***
## 贡献

欢迎任何形式的贡献！如果你有任何问题或者建议，请提交 issue 或者 pull request。

## 许可

这个包遵循 MIT 许可。

