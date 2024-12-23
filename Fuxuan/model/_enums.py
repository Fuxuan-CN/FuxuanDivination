
from enum import StrEnum

class IttrType(StrEnum):
    """占卜类型"""
    LUCK = "luck" # 吉凶
    ITEM = "item" # 寻物
    LOVE = "love" # 爱情
    WEATHER = "weather" # 天气
    WORK = "work" # 工作
    MONEY = "money" # 财运
    FAMILY = "family" # 家庭
    ANOTHER = "another" # 其他，通常是默认的占卜方式，比如不知道是什么占卜，则默认使用这个
    NONE = "none" # 无占卜
    ...

class DivinationType(StrEnum):
    """占卜方式"""
    TIME = "time" # 时间
    NUMBER = "number" # 数字
    ...