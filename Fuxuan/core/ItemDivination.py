
from ..utils import ACQUIRED_HEXGRAM , INHERENT_HEXGRAM
import random
from ..interface.divination import DivinationAble

class ItemDivination(DivinationAble):
    """ 寻物占卜 """

    def __init__(self) -> None:
        self.before = INHERENT_HEXGRAM # 先天卦
        self.after = ACQUIRED_HEXGRAM # 后天卦

    def get_three_nums(self) -> tuple[int, int, int]:
        """获取三个数字"""
        first = random.randint(1, 8)
        second = random.randint(1, 8)
        third = random.randint(1, 8)
        return first, second, third