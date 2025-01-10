""" AI处理器，用于处理AI相关的功能 """

from ...interface.ai_handler import AIHandler
from ._zhipu_ai import Session

class ZhipuAIHandler(AIHandler):
    """ 基于质谱AI的AI处理器 """

    def __init__(self, model_name: str, api_key: str, stream: bool = True) -> None:
        self.session = Session(model_name, api_key, stream=stream)
        print(f"当前使用解卦的处理器类型: {self.__class__.__name__}")

    def send(self, usr_message: str, output_to_console: bool = True, *args, **kwargs) -> str:
        """ 发送消息给AI """
        return self.session.send(usr_message, output_to_console, *args, **kwargs)
    
    def load_another_system_prompt(self, prompts: list[str]) -> None:
        """ 加载系统提示 """
        self.session.load_another_system_prompt(prompts)