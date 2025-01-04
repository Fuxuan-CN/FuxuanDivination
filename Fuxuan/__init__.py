""" 占卜模块 """

from .core import Interpretation , Num, Divinator , exechooks
from .utils import CalculateEightChar
from .model import IttrType , DivinationType, DivinationQuestion


__all__ = [
    'CalculateEightChar', 
    'Interpretation', 
    'Num', 'Divinator', 
    'DivinationType', 'IttrType',
    'exechooks', 'DivinationQuestion'
]