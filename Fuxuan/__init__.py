""" 占卜模块 """

from .core import Interpretation , Num, Divinator , exechooks
from .model import IttrType , DivinationType, DivinationQuestion


__all__ = [
    'Interpretation', 
    'Num', 'Divinator', 
    'DivinationType', 'IttrType',
    'exechooks', 'DivinationQuestion'
]