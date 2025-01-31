
from ..interface import DivinationAble
from .handler import DIVINATION_HANDLER
from ..model import DivinationType, DivinationResult, DivinationQuestion
from ..exceptions import DivinationHandlerNotFound
from ..metadata import print_logo_and_some_infomation

class Divinator(DivinationAble):
    """
    易经占卜程序的起卦器。
    本人符玄厨QwQ~
    """
    def __init__(self) -> None:
        self._handler = DIVINATION_HANDLER
        print_logo_and_some_infomation()

    def run(self, question: DivinationQuestion, div_method: DivinationType, *args, **kwargs) -> tuple[DivinationResult, str]:
        handler = self._handler.get(div_method, None)
        if not handler:
            raise DivinationHandlerNotFound(f"根据占卜方法 {div_method} 没有找到对应的占卜处理器程序")
        else:
            handler_instance = handler(*args, **kwargs)
            result = handler_instance.handle(question)
            return result