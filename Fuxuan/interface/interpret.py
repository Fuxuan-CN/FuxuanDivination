
from abc import ABC , abstractmethod
from typing import Optional
from ..model import DivinationResult , IttrType  , DivinationComment, DivinationQuestion

class InterpretHandler(ABC):
    """
    解卦处理器(接口)
    """

    @abstractmethod
    def set_api_key(self, api_key: str) -> None:
        """设置API密钥"""
        pass

    @abstractmethod
    def get_div_type(self) -> IttrType:
        """获取占卜类型"""
        pass

    @abstractmethod
    def __call__(self, div_result: DivinationResult, *args, **kwargs) -> Optional[str | DivinationComment]:
        """解卦"""
        pass

    @abstractmethod
    def handle(self, div_result: DivinationResult, question: DivinationQuestion, *args, **kwargs) -> Optional[str | DivinationComment]:
        """解卦"""
        pass
    
class InterpretAble(ABC):
    """
    解卦抽象类(接口)
    """

    @abstractmethod
    def get_handler(self, div_type: IttrType) -> InterpretHandler:
        """获取占卜处理器"""
        pass

    @abstractmethod
    def interpret(self, div_result: DivinationResult, *args, **kwargs) -> Optional[str]:
        """解卦"""
        pass