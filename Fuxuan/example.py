""" 示例代码 """

from . import Num, Divinator, DivinationQuestion
from . import Interpretation, DivinationType , IttrType
import os

def main() -> None:
    """ 主函数 """
    divinator = Divinator()
    avaliable_div_methods = list(DivinationType.__members__.keys())
    avaliable_question_types = list(IttrType.__members__.keys())
    question = input("请输入占卜问题：").strip()
    if not os.path.exists("api_key.key"):
       api_key = input("请输入API Key：").strip()
       with open("api_key.key", "w") as key_file:
           key_file.write(api_key)
    else:
       with open("api_key.key") as key_file:
           api_key = key_file.read().strip()
    div_t = input(f"请输入占卜类型({'/'.join(avaliable_question_types)})：").strip().lower()
    div_method = input(f"请输入占卜方法({'/'.join(avaliable_div_methods)})：").strip().lower()
    ittr = Interpretation(api_key)
    _question = DivinationQuestion(question, div_method) # type: ignore

    if div_method == "number" or div_method == "num":
        number1 = int(input("请输入第一个数字：").strip())
        number2 = int(input("请输入第二个数字：").strip())
        number3 = int(input("请输入第三个数字：").strip())
        num = Num(number1, number2, number3)
        result, hexagram_readable = divinator.run(_question, DivinationType.NUMBER, num)
    else:
        result, hexagram_readable = divinator.run(_question, div_method) # type: ignore
    print(hexagram_readable)
    ittr.interpret(result, div_t, _question, auto_match_type=True, output_to_file=True, output_to_console=True) #type: ignore