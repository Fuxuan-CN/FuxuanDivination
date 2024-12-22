
from enum import StrEnum

class IttrType(StrEnum):
    """占卜类型"""
    LUCK = "luck" # 吉凶
    ITEM = "item" # 寻物
    NONE = "none" # 无占卜
    ...

class DivinationType(StrEnum):
    """占卜方式"""
    TIME = "time" # 时间
    NUMBER = "number" # 数字
    ...