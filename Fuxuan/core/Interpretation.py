from typing import Optional
from ..interface.Interpret import InterpretHandler
from ..model import DivinationResult , DivinationComment, DivinationQuestion
from ..interface.Interpret import InterpretAble
from ..model import IttrType
from ..exceptions import ErrorUsage, NotImplementFunctional
from .handler.IttrHandlers import HANDLER_DICT
from datetime import datetime

class Interpretation(InterpretAble):
    """
    解卦类, 用于解释卦象
    """

    def __init__(self, api_key: str = "your_api_key") -> None:
        self.api_key = api_key

    def get_handler(self, div_type: IttrType) -> InterpretHandler | None:

        handlerType = HANDLER_DICT.get(div_type)
        if not handlerType:
            return None
        inst = handlerType(self.api_key) # type: ignore
        return inst

    def interpret(self, 
        div_result: DivinationResult,
        div_type: IttrType,
        question: DivinationQuestion,
        auto_match_type: bool = False,
        output_to_file: bool = False,
        output_to_console: bool = True,
        *args: Optional[list],
        **kwargs: Optional[dict]
    ) -> Optional[str | DivinationComment]:
        """
        解释卦象(解释卦象的主函数)
        - div_result: 卦象结果
        - div_type: 解释卦象的类型
        - question: 问题
        - auto_match_type: 是否自动匹配问题问的类型
        - output_to_file: 是否输出到文件
        - **kwargs: 其他参数
        """
        if not auto_match_type:
            if not question.validate():
                raise ErrorUsage(f"你问的问题: '{question.content}，似乎与问题的类型 {div_type} 无关，请重新输入或指定占卜类型。")
        else:
            div_type = question.auto_type()
            print(f"自动匹配到占卜类型: {div_type.value}")
                
        handler = self.get_handler(div_type)

        if not handler:
            raise NotImplementFunctional(f"占卜处理器: {div_type.value} 尚未实现，请等开发者更新。")
            
        answer = handler.handle(div_result, question=question, output_to_console=output_to_console) # type: ignore
        if output_to_file:
            with open(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{div_type.value}.txt", "w", encoding="utf-8") as f:
                f.write(str(answer))

        return answer