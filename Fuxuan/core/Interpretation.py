from typing import Optional
import re
from ..interface.Interpret import InterpretHandler
from ..model import DivinationResult , DivinationComment
from ..interface.Interpret import InterpretAble
from ..model import IttrType
from ..exceptions import ErrorUsage
from .handler.IttrHandlers import HANDLER_DICT
from datetime import datetime

class Interpretation(InterpretAble):
    """
    解卦类, 用于解释卦象
    """

    def __init__(self, api_key: str = "your_api_key") -> None:
        self.api_key = api_key

    def get_handler(self, div_type: IttrType) -> InterpretHandler | None:
        handler = HANDLER_DICT.get(div_type)(self.api_key) # type: ignore
        return handler
    
    def easy_usage_judge(self, question: str, div_type: IttrType) -> bool:
        """
        简单的判断使用方法是否正确，使用正则表达式进行更复杂的匹配
        """
        item_pattern = r"寻物|物品|物体|寻找|找|东西|丢失|丢|落下|落|找到|捡到"
        luck_pattern = r"运势|命运|运气|吉凶|运|好运"
        if div_type == IttrType.ITEM:
            return bool(re.search(item_pattern, question, re.IGNORECASE))
        elif div_type == IttrType.LUCK:
            return bool(re.search(luck_pattern, question, re.IGNORECASE))
        return False

    def match_type(self, question: str) -> IttrType:
        """
        匹配占卜类型
        """
        item_pattern = r"寻物|物品|物体|寻找|找|东西|丢失|丢|落下|落|找到|捡到"
        luck_pattern = r"运势|命运|运气|吉凶|运|好运"
        if re.search(item_pattern, question, re.IGNORECASE):
            return IttrType.ITEM
        elif re.search(luck_pattern, question, re.IGNORECASE):
            return IttrType.LUCK
        return IttrType.NONE

    def interpret(self, 
        div_result: DivinationResult,
        div_type: IttrType,
        question: str,
        auto_match_type: bool = True,
        output_to_file: bool = False,
        **kwargs: Optional[dict]
    ) -> Optional[DivinationResult | str | DivinationComment]:
        """
        解释卦象(解释卦象的主函数)
        """
        if not auto_match_type:
            if not self.easy_usage_judge(question, div_type):
                suggested_type = self.match_type(question)
                raise ErrorUsage(f"请使用正确的占卜方式或类型，你选择的类型：{div_type}，但似乎问题: '{question}' 与该占卜类型不相干。建议使用 {suggested_type} 类型。")
        else:
            # 自动匹配占卜类型
            original_type = div_type
            div_type = self.match_type(question)
            if div_type != original_type:
                print(f"注意：根据问题 '{question}'，已自动选择 {div_type} 类型，而不是用户指定的 {original_type} 类型。")
                
        if div_type not in HANDLER_DICT.keys() or div_type == IttrType.NONE:
            # 不指定占卜类型或占卜类型无效, 则直接返回卦象结果
            return div_result
        handler = self.get_handler(div_type)
        if not handler:
            raise NotImplementedError(f"Handler for {div_type} not implemented")
        answer = handler.handle(div_result, question=question)
        if output_to_file:
            with open(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{div_type.value}.txt", "w", encoding="utf-8") as f:
                f.write(str(answer))

        return answer