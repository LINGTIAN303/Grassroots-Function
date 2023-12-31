import requests


class APIConnector:
    def __init__(self, base_url):
        self.base_url = base_url

def call_api(self, endpoint, method, parameters):
    """
    使用指定的终结点、方法和参数调用 API。

    Args:
        endpoint (str): 要调用的 API 终结点。
        method (str): 要使用的 HTTP 方法 (“GET”或“POST”)。
        parameters (dict): 要随请求一起发送的参数。

    Returns:
        dict or None: 来自 API 的 JSON 响应, 如果出现错误, 则为“None”。

    Raises:
        Exception: 如果进行 API 调用时出错。
    """
    url = self.base_url + endpoint

    try:
        if method.lower() == 'get':
            response = requests.get(url, params=parameters)
        elif method.lower() == 'post':
            response = requests.post(url, data=parameters)
        else:
            print("Unsupported method")
            return None

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error in API call: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error in API call: {e}")
        return None
