""" 给SRA写的一个插件，属于扩展 """

from .. import Num, Divinator, DivinationQuestion
from .. import Interpretation, DivinationType , IttrType
from ..model import DivinationResult, DivinationComment
from ..utils.ai import ZhipuAIHandler
from typing import Optional
from ..exceptions import DivinationError

class SRADivinationPlugin:
    """ 给SRA写的占卜插件 """

    def __init__(self, api_key: str) -> None:
        self.divinator = Divinator()
        self.iterper = Interpretation(ZhipuAIHandler(model_name="glm-4v-flash", api_key=api_key, stream=False))
        self.asked_cache: tuple[DivinationResult, str, DivinationQuestion] = None # type: ignore

    def get_divination_methods(self) -> list[str]:
        """获取可用的占卜方法"""
        return list(DivinationType.__members__.keys())
    
    def get_interpreter_methods(self) -> list[str]:
        """获取可用的解卦方法"""
        return list(IttrType.__members__.keys())

    def ask(self, question: str, question_type: IttrType, divination_method: DivinationType, *args, **kwargs) -> None:
        """占算中的提问，然后生成卦象
        - question: 问题
        - question_type: 你问的问题是属于什么类型？ 比如运势 luck, 爱情 love, 财富 money, 工作 work等...
        - divination_method: 你想用什么方法占卜？比如 num(数字), time(时间) ...
        - args: 额外传参，比如数字占卜时，需要传入数字,比如 1, 2, 3
        - kwargs: 额外传参，比如数字占卜时，需要传入数字对应的键值, first_num=1, second_num=2, third_num=3
        """
        _question = DivinationQuestion(question, question_type)
        if divination_method == DivinationType.NUMBER:
            num = Num(*args, **kwargs)
            result = self.divinator.run(_question, divination_method, num)
        else:
            result = self.divinator.run(_question, divination_method)
        self.asked_cache = result + (_question,) # 缓存结果
    
    def get_answer(self, auto_match_type=True, output_to_file=True, output_to_console=False, *args, **kwargs) -> Optional[DivinationComment | str]:
        """获取占算结果 
        - auto_match_type: 当开始解卦的时候会进行类型验证，如果验证不通过会抛出ErrorUsage异常，开启这个会自动进行类型匹配
        - output_to_file: 是否输出到文件
        - output_to_console: 是否输出到控制台
        - args: 额外传参
        - kwargs: 额外传参
        """
        if self.asked_cache is None:
            DivinationError("请先提问")
        _result , hexagram_readable, question = self.asked_cache
        result = self.iterper.interpret(_result, question.type, question, auto_match_type, output_to_file, output_to_console, *args, **kwargs)
        return result