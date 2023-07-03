import unittest
from model_interaction import ModelInteraction


class TestModelInteraction(unittest.TestCase):
    def setUp(self):
        self.mi = ModelInteraction("test_openai_api_key")

    def test_call_model(self):
        # 我们只是要测试该方法是否存在并且不会出错
        # 在实际测试中，您需要模拟对OpenAI API的调用，并测试它是否正确调用。
        try:
            self.mi.call_model("Test input", [])
        except Exception as e:
            self.fail(f"call_model raised an exception: {e}")

    def test_handle_response(self):
        # 同样，这是一个非常简单的测试
        # 在实际测试中，您希望使用不同的输入测试此方法并检查其输出
        try:
            self.mi.handle_response({"choices": [{"message": {"function_call": {}}}]})
        except Exception as e:
            self.fail(f"handle_response raised an exception: {e}")

    # 为 ModelInteraction 类中的其他方法添加更多测试


if __name__ == '__main__':
    unittest.main()
