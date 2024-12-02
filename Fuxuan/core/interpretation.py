from typing import Optional

from Fuxuan.interface.interpret import InterpretHandler
from ..model import DivinationResult
from ..interface.interpret import InterpretAble
from ..model import DivType
from .handlers import LuckHandler

class Interpretation(InterpretAble):
    """
    解卦类, 用于解释卦象
    """

    def __init__(self) -> None:
        self.handler_type_dict = {
            DivType.LUCK: LuckHandler()
        }

    def get_handler(self, div_type: DivType) -> InterpretHandler:
        return self.handler_type_dict[div_type]

    def interpret(self, 
        div_result: DivinationResult,
        output_to_console: bool = True, # 是否输出到控制台
        out_to_file: bool = False, # 是否输出到文件
        file_path: str = "interpretation.txt" # 文件路径
    ) -> Optional[str]:
        """
        解释卦象(解释卦象的主函数)
        """
        handler = self.get_handler(div_result.div_type)
        answer = handler.handle(div_result)

        if output_to_console:
            print(answer)
        if out_to_file and isinstance(answer, str):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(answer)
        return answer