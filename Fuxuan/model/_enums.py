
from enum import StrEnum

class DivType(StrEnum):
    """占卜类型"""
    LUCK = "luck" # 吉凶
    ITEM = "item" # 寻物
    NONE = "none" # 无占卜
    ...