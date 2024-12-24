
from dataclasses import dataclass, field
from ._enums import IttrType
import re

@dataclass
class DivinationQuestion:
    """ 占卜的问题 """
    content: str
    type: IttrType
    meta: dict[str, str] = field(default_factory=lambda: {})
    _patten_keywords: dict[IttrType, str] = field(default_factory=lambda: {
        IttrType.ITEM: r"寻物|物品|物体|寻找|找|东西|丢失|丢|落下|落|找到|捡到",
        IttrType.LUCK: r"运势|命运|运气|吉凶|运|好运",
        IttrType.LOVE: r"爱情|恋爱|情人节|情侣|情|爱|女朋友|关系|男朋友|宝|伴侣|小三|桃花运",
        IttrType.WEATHER: r"天气|气象|天有不测风云",
        IttrType.WORK: r"工作|职业|事业|事|工作岗位|工作情况|工作状态|工作环境|职位|升官|官场|职场",
        IttrType.MONEY: r"财富|钱财|金钱",
        IttrType.FAMILY: r"家庭|家人|老公|老婆|父母|孩子|爷爷|奶奶|爸爸|妈妈",
    })

    def validate(self) -> bool:
        """
        简单的判断使用方法是否正确，使用正则表达式进行更复杂的匹配
        """
        patten = self._patten_keywords.get(self.type)
        if not patten:
            return False
        return bool(re.search(patten, self.content, re.IGNORECASE))
    
    def auto_type(self) -> IttrType:
        """
        根据问题自动判断问题类型
        """
        for div_type, patten in self._patten_keywords.items():
            if re.search(patten, self.content, re.IGNORECASE):
                return div_type
        return IttrType.ANOTHER
    
    def __str__(self) -> str:
        return self.content