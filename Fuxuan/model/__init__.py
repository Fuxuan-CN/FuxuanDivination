""" 数据模型 """

from ._result import DivinationResult, DivinationComment
from ._type import hexagramType, hexagramsType
from ._enums import DivType

__all__ = ['DivinationResult', 'hexagramType', 'hexagramsType', 'DivType', 'DivinationComment']