""" AI处理器的接口 """
from abc import ABC, abstractmethod


class AIHandler(ABC):
    """ AI处理器的接口 """

    @abstractmethod
    def load_another_system_prompt(self, prompts: list[str]) -> None:
        """
        加载其他系统的提示
        """
        pass

    @abstractmethod
    def send(self, usr_message: str, output_to_console: bool, *args, **kwargs) -> str:
        """
        处理用户输入，返回AI回复
        """
        pass