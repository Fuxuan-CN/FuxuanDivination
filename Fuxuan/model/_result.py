
from dataclasses import dataclass
from ._type import hexagramsType
from ._enums import DivType

@dataclass
class DivinationResult:
    """占卜结果"""
    div_type: DivType
    original: hexagramsType
    mutual: hexagramsType
    changed: hexagramsType