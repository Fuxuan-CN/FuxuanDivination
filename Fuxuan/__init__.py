""" 占卜模块 """

from .core import TimeDivination , Interpretation , Num , NumDivination
from .utils import CalculateEightChar
from .model import DivType


__all__ = [
    'TimeDivination', 'CalculateEightChar', 
    'Interpretation', 
    'Num', 'NumDivination', 
    'DivType'
]