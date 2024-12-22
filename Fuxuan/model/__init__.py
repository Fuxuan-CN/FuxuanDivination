""" 数据模型 """

from ._result import DivinationResult, DivinationComment
from ._type import hexagramType, hexagramsType
from ._enums import DivinationType , IttrType

__all__ = ['DivinationResult', 'hexagramType', 'hexagramsType', 'DivinationType', 'IttrType', 'DivinationComment']