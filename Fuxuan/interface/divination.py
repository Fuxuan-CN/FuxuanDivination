
from abc import ABC , abstractmethod
from ..model import DivinationResult

class DivinationAble(ABC):
    """
    占卜抽象类(接口)
    """
    
    @abstractmethod
    def build_hexagram(self) -> DivinationResult:
        """构建卦象"""
        pass

    @abstractmethod
    def run(self, question: str) -> tuple[DivinationResult, str]:
        """运行占卜"""
        pass