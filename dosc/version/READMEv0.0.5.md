# 更新：Grassroots Function _v0.0.5_

该版本在原基础上增加了一个`@oa`装饰器，它提供了一个更简单、更直观的方式来定义和使用函数！

## 增加装饰器

新项目的主要组成部分包括：

3. `function_descriptor.py`：包含`FunctionDescriptor`类和`@oa`装饰器，负责描述和管理函数。

## 如何使用

在新版本中，你可以在你的项目中通过以下步骤使用它：

1. 编写`主程序.py`文件中，使用`@oa`装饰器定义你的函数。
2. 运行你的`主程序.py`文件，输入你的对话提示，然后程序将自动处理函数调用和模型交互。

## 主要优化和新增功能

新版本的主要优化和新增功能包括：

1. 自动函数定义：通过`@oa`装饰器，你可以更容易地定义函数，而不需要手动创建函数的定义。
2. 自动函数管理：通过`FunctionDescriptor`类，你可以更容易地管理你的函数，包括添加新的函数和获取所有的函数。
3. 自动模型交互：通过`ModelInteraction`类，你可以更容易地与OpenAI的GPT模型进行交互，包括调用模型、处理模型的响应、将函数调用的结果发送回模型、提取模型的最终消息等。
4. 自动API交互：通过`APIConnector`类，你可以更容易地与外部API进行交互，包括调用API并获取响应。

## 示例代码

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

在这个示例代码中，我们首先导入了新项目，然后我们初始化了`ModelInteraction`和`FunctionDescriptor`类，定义了一些函数，然后我们运行了一个对话，其中包括调用模型和处理模型的响应。

以下是使用新版本的步骤：

## 步骤1：安装包

首先，你需要将新版本安装到你的Python环境中。新项目还没有发布到PyPI，你可以将新项目的代码下载到你的项目的目录中并`pip install`。

## 步骤2：导入包

在你的项目的代码中，使用`import`语句来导入`grassroots_function`。

## 步骤3：初始化类

你需要初始化`ModelInteraction`和`FunctionDescriptor`类。并提供你的OpenAI API密钥来初始化`ModelInteraction`类。

```python
api_key = "your_openai_api_key"
model_interaction = grassroots_function.ModelInteraction(api_key)
function_descriptor = grassroots_function.FunctionDescriptor()
```

## 步骤4：定义函数

你可以使用`@oa`装饰器来定义你的函数。这个装饰器会自动创建函数的描述，并添加到`FunctionDescriptor`类中。

```python
@grassroots_function.oa
def add_numbers(a: int, b: int):
    return a + b

@grassroots_function.oa
def say_hello(name: str):
    return f"Hello, {name}!"
```

## 步骤5：运行对话

你可以使用`ModelInteraction`类的`call_model`方法来运行对话。你需要提供你的对话提示和函数描述。

```python
prompt = input("You: ")
response = model_interaction.call_model(prompt, function_descriptor.get_functions())
print(response)
```

这个方法会自动处理函数调用和模型交互，并返回模型的响应。

以上就是使用新项目的步骤。通过这些步骤，你可以更容易地定义和使用函数，同时也可以更容易地与OpenAI的GPT模型和外部API进行交互。