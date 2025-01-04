
from typing import Literal , Sequence, Any , TypedDict
from pathlib import Path
import sys

if getattr(sys, 'frozen', False):  # 是否Bundle Resource
    CURRENT_DIR = Path(sys.executable).parent.parent.parent
else:
    CURRENT_DIR = Path(__file__).parent.parent.parent

FUXUAN_META_PATH = CURRENT_DIR / "core" / "meta" / "符玄.json"
""" 符玄元数据路径 """
START_SYS_PROMPT = "你是符玄，出生于玉阙仙舟观星士世家的符氏一族。仙舟「罗浮」太卜司之首，自信耿直的智者。凭借第三眼与穷观阵为仙舟占算航路，预卜事务吉凶，坚信自己所做的一切便是事情的“最优解”。符玄等待着将军承诺的“退位让贤”，然而这一天的到来…似乎还遥遥无期。"
""" 初始系统提示 """

class Message(TypedDict):
    role: Literal['user', 'assistant', 'system', 'tool']
    content: str
    images: Sequence[Any]