
from abc import ABC , abstractmethod
from ..model import DivinationResult, DivinationType

class DivinationHandlerAble(ABC):
    """
    占卜处理器(接口)
    """

    @abstractmethod
    def handle(self, question: str) -> tuple[DivinationResult, str]:
        """处理占卜"""
        pass

class DivinationAble(ABC):
    """
    占卜抽象类(接口)
    """

    @abstractmethod
    def run(self, question: str, div_type: DivinationType, *args, **kwargs) -> tuple[DivinationResult, str]:
        """运行占卜"""
        pass