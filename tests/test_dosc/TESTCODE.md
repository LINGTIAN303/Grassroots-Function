# 测试成功文档
***
## 简介
我将使用Alpha vantage作为本次测试用例！

### 步骤一：导入包
首先我创建了一个Python文件导入了`Grassroots Function`：
```bash
import json # 函数所需
import grassroots_function # 导入包

from grassroots_function.api_connector import APIConnector as ac # 以下三条导入是因为我的Python解释器找不到包
from grassroots_function import model_interaction
from grassroots_function.function_descriptor import oa
```
```bash
import sys  # 如果你的 Python 解释器找不到包，你可以像我一样使用 sys 寻找！
sys.path.append("你的包所在路径\grassroots_function")
```
***
### 步骤二：初始化类
随后我使用到了`ModelInteraction`类，该类用于调用模型时配置`openai api key`，并免去编写`openai.ChatCompletion.create`方法：
```python
openai_api_key = "Your_OpenAI_API_KEY"  # 填入你的OpenAI API KEY
model_interaction = grassroots_function.model_interaction.ModelInteraction(openai_api_key)
```
接下来使用到`FunctionDescriptor`类，用于函数描述这部分'也就是发送给GPT时的json架构对象，该类将会免去编写`functions`函数参数，也就是发送给GPT的`name`、`parameters`、`required`等函数参数的字段：
```python
function_descriptor = grassroots_function.function_descriptor.FunctionDescriptor()
```
***
### 步骤三：定义函数
该步骤是请求`Alpha vantage API`，也就是第三方API：

在这一部分中我首先配置了`Alpha vantage API key`，以及`Alpha vantage API URL`：用于发送查询请求
```python
alpha_vantage_api_key = "Your_Alpha-Vantage_API_KEY"
api_connector = ac("https://www.alphavantage.co/query?")
```
其次，我使用`@oa`装饰器包装`get_stock_price`函数，省去函数大部分繁杂的编写定义步骤！
```python
@oa # 包装函数
def get_stock_price(symbol: str):
    parameters = {
        "function": "GLOBAL_QUOTE", # 请求时的函数字段
        "symbol": symbol,  # 由于Alpha vantage API返回的结果股票符号（symbol）被包装在一个额外的字典中，即 'symbol': {'symbol': '股票代码'}，所以此处将直接使用“symbol”，并将函数作出更改！
        "apikey": alpha_vantage_api_key # 上方配置
    }
    response = api_connector.call_api("", "get", parameters)
    print(response) 
    if response: # 用于检查API返回结果状态
        return response["Global Quote"]["05. price"]
    else:
        return "Error in getting stock price"
```
***
### 步骤四：函数描写
此处由于`FunctionDescriptor`类，所以免去`functions`的必须参数，只需要写上描述和跟你的函数所需请求参数类型即可！
```python
function_descriptor.add_function("get_stock_price", "Get the current price of a stock.", {"symbol": {
            "type": "string", "description": "The stock symbol"}}, ["symbol"]) # 由于description在函数描述中是一个JSON字典结构不会自动填充API请求中的参数，所以需要你根据你定义的函数去编写该参数！
```
***
### 步骤五：用户输入
最后让我们运行它：因为是测试，所以这里简单写一个实现用户输入！
```python
# 请求用户输入
prompt = input("You: ")

# 使用用户的输入和定义的函数调用模型
response = model_interaction.call_model(prompt, function_descriptor.get_functions())

# 打印模型的响应
print(response)

# 如果用户的输入以“Get the price of”开头，则获取股票价格
if prompt.startswith("Get the price of "):
    # 从用户输入中提取股票代码
    symbol = prompt.replace("Get the price of ", "")
    
    # 使用提取的符号调用 get_stock_price 函数
    price = get_stock_price({"symbol": symbol})
    
    # 打印股票的当前价格
    print(f"The current price of {symbol} is {price}")

# 处理来自模型的响应
function_call = model_interaction.handle_response(response)

# 如果在模型的响应中进行了函数调用
if function_call:
    # 获取被调用函数的名称
    function_name = function_call["name"]
    
    # 解析传递给函数的参数
    arguments = json.loads(function_call["arguments"])
    
    # 如果调用的函数是get_stock_price
    if function_name == "get_stock_price":
        # 使用解析后的参数调用 get_stock_price 函数
        price = get_stock_price(arguments['symbol'])  # 直接传递“symbol”
        
        # 打印股票的当前价格
        print(f"The current price of {arguments['symbol']} is {price}")

```
***
## 结果
接下来是**整个返回结果**，为了解释，我将每一行分割开！

从OpenAI GPT-3.5-turbo模型返回的响应，它包含了一次对话的结果：

下方`用户输入："获取 AAPL 的价格"`
```commandline
You: get the price of AAPL
```
下方`"id": "chatcmpl-7Z1HTTlJP9xGLoPOvGDZqxzwf2pbF"`：这是此次对话的唯一ID：
```yaml
{
  "id": "chatcmpl-7Z1HTTlJP9xGLoPOvGDZqxzwf2pbF",
```
下方`"object": "chat.completion"`：这表示返回的对象类型是一个聊天完成对象：
```yaml
  "object": "chat.completion",
```
下方`"created": 1688580759`：这是此次对话创建的Unix时间戳:
```python
  "created": 1688580759,
```
下方`"model": "gpt-3.5-turbo-0613"`：这表示使用的模型是GPT-3.5-turbo：
```yaml
  "model": "gpt-3.5-turbo-0613",
```
下方`"choices": [...]`：这是模型生成的响应列表。在这个例子中，只有一个响应：
```bash
  "choices": [
    {
```
下方`"index": 0`：这是响应的索引。
```yaml
      "index": 0,
```
下方`"message": {...}`：这是模型生成的消息。
```yaml
      "message": {
```
下方`"role": "assistant"`：这表示消息的角色是助手。
```yaml
        "role": "assistant",
```
下方`"content": null`：这表示助手的消息内容为空，因为它执行了一个函数调用。
```yaml
        "content": null,
```
下方`"function_call": {...}`：这是助手执行的函数调用。
```python
        "function_call": {
```
下方`"name": "get_stock_price"`：这是被调用的函数的名称。
```yaml
          "name": "get_stock_price",
```
下方`"arguments": "{\n  \"symbol\": \"AAPL\"\n}"`：这是传递给函数的参数。
```yaml
          "arguments": "{\n  \"symbol\": \"AAPL\"\n}"
        }
      },
```
下方`"finish_reason": "function_call"`：这表示对话因为函数调用而结束。
```bash
      "finish_reason": "function_call"
    }
  ],
```
下方`"usage": {...}`：这是此次对话的用量统计。
```commandline
  "usage": {
```
下方`"prompt_tokens": 59`：这是提示使用的令牌数。
```commandline
    "prompt_tokens": 59,
```
下方`"completion_tokens": 17`：这是生成的响应使用的令牌数。
```commandline
    "completion_tokens": 17,
```
下方`"total_tokens": 76`：这是总共使用的令牌数。
```commandline
    "total_tokens": 76
  }
}
```
下方的URL和参数是`定义函数这部分`的代码向`Alpha Vantage API`发出的请求。
```commandline
https://www.alphavantage.co/query? {'function': 'GLOBAL_QUOTE', 'symbol': 'AAPL', 'apikey': '此处为包含这密钥的返回值'}
```
下方的字典是从`Alpha Vantage API`返回的股票报价信息，包括股票符号、开盘价、最高价、最低价、当前价格、交易量等。
```commandline
{'Global Quote': {'01. symbol': 'AAPL', '02. open': '193.7800', '03. high': '193.8800', '04. low': '191.7600', '05. price': '192.4600', '06. volume': '31458198', '07. latest trading day': '2023-07-03', '08. previous close': '193.9700', '09. change': '-1.5100', '10. change percent': '-0.7785%'}}
```
下方`The current price of AAPL is 192.4600`是GPT调用函数后的API返回并打印出的消息，表示苹果公司`AAPL`的当前股票价格是192.46美元。
```commandline
The current price of AAPL is 192.4600
```
***
## 完整一页代码和返回结果
### 代码
```python
import sys
import json

from grassroots_function.api_connector import APIConnector as ac
sys.path.append("你的包所在路径\grassroots_function")
import grassroots_function
from grassroots_function import model_interaction
from grassroots_function.function_descriptor import oa

# Initialize the classes
openai_api_key = "Your_OpenAI_API_KEY"
model_interaction = grassroots_function.model_interaction.ModelInteraction(openai_api_key)
function_descriptor = grassroots_function.function_descriptor.FunctionDescriptor()

# Define your functions
@oa
def add_numbers(a: int, b: int):
    return a + b

@oa
def say_hello(name: str):
    return f"Hello, {name}!"

alpha_vantage_api_key = "Your_Alpha-Vantage_API_KEY"  # Replace with your Alpha Vantage API key
api_connector = ac("https://www.alphavantage.co/query?")

@oa
def get_stock_price(symbol: str):
    parameters = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,  # Use 'symbol' directly
        "apikey": alpha_vantage_api_key
    }
    response = api_connector.call_api("", "get", parameters)
    print(response)
    if response:
        return response["Global Quote"]["05. price"]
    else:
        return "Error in getting stock price"

function_descriptor.add_function(
    "get_stock_price", "Get the current price of a stock.", 
    {
        "symbol": 
        {
            "type": "string", "description": "The stock symbol"
            }
            }, 
            ["symbol"]
            )

# Run the conversation
prompt = input("You: ")
response = model_interaction.call_model(prompt, function_descriptor.get_functions())
print(response)
if prompt.startswith("Get the price of "):
    symbol = prompt.replace("Get the price of ", "")
    price = get_stock_price({"symbol": symbol})
    print(f"The current price of {symbol} is {price}")

function_call = model_interaction.handle_response(response)
if function_call:
    function_name = function_call["name"]
    arguments = json.loads(function_call["arguments"])
    if function_name == "get_stock_price":
        price = get_stock_price(arguments['symbol'])  # Pass 'symbol' directly
        print(f"The current price of {arguments['symbol']} is {price}")
```

### 返回结果

```yaml
You: get the price of AAPL
{
  "id": "chatcmpl-7Z1HTTlJP9xGLoPOvGDZqxzwf2pbF",
  "object": "chat.completion",
  "created": 1688580759,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "function_call": {
          "name": "get_stock_price",
          "arguments": "{\n  \"symbol\": \"AAPL\"\n}"
        }
      },
      "finish_reason": "function_call"
    }
  ],
  "usage": {
    "prompt_tokens": 59,
    "completion_tokens": 17,
    "total_tokens": 76
  }
}
https://www.alphavantage.co/query? {'function': 'GLOBAL_QUOTE', 'symbol': 'AAPL', 'apikey': '此处为包含这密钥的返回值'}
{'Global Quote': {'01. symbol': 'AAPL', '02. open': '193.7800', '03. high': '193.8800', '04. low': '191.7600', '05. price': '192.4600', '06. volume': '31458198', '07. latest trading day': '2023-07-03', '08. previous close': '193.9700', '09. change': '-1.5100', '10. change percent': '-0.7785%'}}
The current price of AAPL is 192.4600
```