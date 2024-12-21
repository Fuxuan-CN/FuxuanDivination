from typing import Optional
import re
from ..interface.interpret import InterpretHandler
from ..model import DivinationResult , DivinationComment
from ..interface.interpret import InterpretAble
from ..model import DivType
from .handlers import LuckHandler, ItemFoundHandler
from ..exceptions import ErrorUsage

class Interpretation(InterpretAble):
    """
    解卦类, 用于解释卦象
    """

    def __init__(self, api_key: str = "your_api_key") -> None:
        self.handler_type_dict = {
            DivType.LUCK: LuckHandler(api_key),
            DivType.ITEM: ItemFoundHandler(api_key)
        }

    def get_handler(self, div_type: DivType) -> InterpretHandler | None:
        return self.handler_type_dict.get(div_type, None)
    
    def easy_usage_judge(self, question: str, div_type: DivType) -> bool:
        """
        简单的判断使用方法是否正确，使用正则表达式进行更复杂的匹配
        """
        if div_type == DivType.ITEM:
            # 匹配寻物相关的各种表达方式
            return bool(re.search(r"寻物|物品|物体|寻找|找", question, re.IGNORECASE))
        elif div_type == DivType.LUCK:
            # 匹配运势相关的各种表达方式
            return bool(re.search(r"运势|命运|运气|吉凶|运", question, re.IGNORECASE))
        return False

    def interpret(self, 
        div_result: DivinationResult,
        div_type: DivType,
        question: str,
        **kwargs: Optional[dict]
    ) -> Optional[DivinationResult | str | DivinationComment]:
        """
        解释卦象(解释卦象的主函数)
        """
        if not self.easy_usage_judge(question, div_type):
            raise ErrorUsage(f"请使用正确的占卜方式或类型，你选择的类型：{div_type}，但似乎问题: '{question}' 与该占卜类型不相干。")
        if div_type not in self.handler_type_dict or div_type == DivType.NONE:
            # 不指定占卜类型或占卜类型无效, 则直接返回卦象结果
            return div_result
        handler = self.get_handler(div_type)
        if not handler:
            raise NotImplementedError(f"Handler for {div_type} not implemented")
        answer = handler.handle(div_result, question=question)
        return answer