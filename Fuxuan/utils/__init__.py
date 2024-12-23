""" 工具模块 """

from .const import NOW, ZHI_TO_TIME, ZHI_NUM, HEXGRAM_DESCRIPTION, YANG, YIN , TIANGAN , DIZHI , TIANGAN_NUM , WUXING , HEXGRAM_TO_WUXING
from .const import DESC_HEXGRAM_TONUM , NUM_TO_HEXGRAM_STR , WUXING_RELATION , generate_wuxing_relation
from .const import RELATION_TO_LUCK
from .const import HEXAGRAM_TO_STR
from .const import HEXGRAM_NUM , HEXAGRAM_DESCRIPTION_STR
from .hexagramsDict import HEXAGRAMS_64_TO_NAME , NAME_TO_HEXAGRAMS_64
from .Correspondences import HEXAGRAM_CORRESPONDENCES
from .const import ACQUIRED_HEXGRAM , INHERENT_HEXGRAM
from .EightChar import CalculateEightChar
from .helpers import Deprecated # 弃用装饰器

generate_wuxing_relation()
__all__ = [
    'NOW', 'ZHI_TO_TIME', 'ZHI_NUM', 'HEXGRAM_DESCRIPTION', 'YANG', 'YIN', 'TIANGAN', 'DIZHI', 'TIANGAN_NUM', 'WUXING',
    'HEXGRAM_TO_WUXING', 'DESC_HEXGRAM_TONUM', 'NUM_TO_HEXGRAM_STR', 'HEXAGRAMS_64_TO_NAME', 'NAME_TO_HEXAGRAMS_64',
    'Deprecated', 'HEXAGRAM_CORRESPONDENCES', 'WUXING_RELATION', 'RELATION_TO_LUCK', 'HEXGRAM_NUM', 'HEXAGRAM_DESCRIPTION_STR',
    'CalculateEightChar', 'ACQUIRED_HEXGRAM', 'INHERENT_HEXGRAM', "HEXAGRAM_TO_STR"
]