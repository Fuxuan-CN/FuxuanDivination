""" 占卜模块 """

from .core import Interpretation , Num, Divinator
from .utils import CalculateEightChar
from .model import IttrType , DivinationType


__all__ = [
    'CalculateEightChar', 
    'Interpretation', 
    'Num', 'Divinator', 
    'DivinationType', 'IttrType'
]