from ...utils import WUXING , HEXGRAM_TO_WUXING , HEXAGRAMS_64_TO_NAME , WUXING_RELATION , RELATION_TO_LUCK
from ...utils import ACQUIRED_HEXGRAM , INHERENT_HEXGRAM, HEXAGRAM_TO_STR
from ...model import hexagramsType, hexagramType, IttrType , DivinationResult , DivinationComment, DivinationQuestion
from ...interface.interpret import InterpretHandler
from ...interface.ai_handler import AIHandler
from typing import Union , Optional
from functools import wraps

HANDLER_DICT: dict[IttrType, type[InterpretHandler]] = {}
"""
解释器字典，用于存储不同类型的解释器
"""
# 实现一个装饰器，用于注册解释器
def Handler(div_type: IttrType):
    @wraps(Handler)
    def wrapper(cls):
        HANDLER_DICT[div_type] = cls # 不实例化，直接存储类
        return cls
    return wrapper

class BaseHandler(InterpretHandler):
    """
    基础解释器，用于处理未知类型解释器
    """
    def __init__(self, handler: AIHandler, type: IttrType = IttrType.NONE) -> None:
        self._type = type # 占卜类型
        self.ai_interpreter_session = handler # 调用外部AI接口
        self.ai_interpreter_session.load_another_system_prompt(["注意，卦象的解释尽可能的详细，长一些的文字都好，并且要确保正确，还有不能输出特殊字符，卦象表示不要用特殊字符，而是用名字，不要重复"])

    def get_name_of_hexagram(self, hexagram: hexagramType) -> str:
        """
        获取卦象的名称
        """
        try:
            hexagram_name = HEXAGRAM_TO_STR[hexagram]
            return hexagram_name
        except KeyError:
            return "未知八卦中的卦象"
        
    def get_64_hexagram(self, hexagram: hexagramsType) -> str:
        """
        获取卦象的类型
        """
        try:
            return HEXAGRAMS_64_TO_NAME[hexagram]
        except KeyError:
            return "卦象还未被收录"

    def get_wuxing_info(self, hexagram: hexagramType, return_wuxing: bool = False) -> Union[dict[str, str], str]:
        """
        获取卦象的五行属性信息 (也是卦象相生相克的信息)
        如果 return_key 为 True, 则返回五行属性
        """
        try:
            hexagram_name = self.get_name_of_hexagram(hexagram)
            wuxing = HEXGRAM_TO_WUXING[hexagram_name]
            hexagram_wuxing_info = WUXING[wuxing]
            # 如果 return_key 为 True, 则返回五行属性的键值
            if return_wuxing:
                return wuxing
            else:
                return hexagram_wuxing_info
        except KeyError:
            return "未知五行属性或卦象"

    def get_div_type(self) -> IttrType:
        return self._type

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key

    def __call__(self, div_result: DivinationResult, *args, **kwargs) -> Optional[DivinationComment | str]:
        return self.handle(div_result, *args, **kwargs)

    def handle(self, div_result: DivinationResult, question: DivinationQuestion, *args, **kwargs) -> Optional[str | DivinationComment]:
        """解卦"""
        raise NotImplementedError("子类必须实现 handle 方法")

@Handler(IttrType.LUCK)
class LuckHandler(BaseHandler):
    """吉凶处理器"""

    def __init__(self, handler: AIHandler) -> None:
        super().__init__(handler, IttrType.LUCK)

    def is_ti_or_yong_hexagram(self,
        original_hexagram: hexagramsType,
        changed_hexagram: hexagramsType
    ) -> dict[str, hexagramType]:
        """
        根据本卦和变卦判断体用关系
        判断方法:
        如果卦象中有变爻,那么为用,否则为体
        """
        ti_or_yong = {}
            # 判断哪个爻变了
        for i in range(6):
            if original_hexagram[i] != changed_hexagram[i]:
                # 如果找到了变爻，则开始拆分
                if i <= 3:
                    # 取上卦
                    ti_or_yong['体'] = original_hexagram[:3] # 体
                    ti_or_yong['用'] = changed_hexagram[3:] # 用
                else:
                    # 取下卦
                    ti_or_yong["体"] = original_hexagram[3:] # 体
                    ti_or_yong["用"] = changed_hexagram[:3] # 用
                break
        return ti_or_yong
    
    # 定义判断相生相克的函数
    def validate_defnense_wuxing_element(self, hexagram_ti: hexagramType, hexagram_yong: hexagramType) -> hexagramType:
        """
        判断两个卦象是否相生相克
        返回 (体/用, 生/克 , 体/用)
        """
        default = ("体", "未知", "用")
        default_reverse = ("用", "未知", "体")
        hexagram_ti_name = self.get_name_of_hexagram(hexagram_ti)
        hexagram_yong_name = self.get_name_of_hexagram(hexagram_yong)

        relation = WUXING_RELATION.get((hexagram_ti_name, hexagram_yong_name), default)
        if relation == default:
            # 未找到对应关系, 尝试反向查找
            relation = WUXING_RELATION.get((hexagram_yong_name, hexagram_ti_name), default_reverse)
        return relation
        
    def interpret_luck_for_hexagram(self, hexagram_ti: hexagramType, hexagram_yong: hexagramType) -> str:
        """
        解释卦象的吉凶
        """
        try:
            relation = self.validate_defnense_wuxing_element(hexagram_ti, hexagram_yong)
            luck = RELATION_TO_LUCK[relation]
            return luck
        except KeyError:
            return "未知吉凶"
        
    def __call__(self, div_result: DivinationResult, *args, **kwargs) -> Optional[DivinationComment | str]:
        return self.handle(div_result, *args, **kwargs)
        
    def handle(self, div_result: DivinationResult, question: DivinationQuestion, *args, **kwargs) -> Optional[DivinationComment | str]:
        """
        解卦
        """
        original = div_result.original
        mutual = div_result.mutual
        changed = div_result.changed
        orig_64 = self.get_64_hexagram(original)
        mutual_64 = self.get_64_hexagram(mutual)
        changed_64 = self.get_64_hexagram(changed)
        hexagram_info = f"""
        太卜大人，帮我解一下运势卦，谢谢，占算的人的问题是 "{question}"，下面是他占卜的结果：
本卦: {orig_64}
变卦: {changed_64}
互卦: {mutual_64}
五行属性: \n
本卦: 上{self.get_wuxing_info(original[:3], True)} 下{self.get_wuxing_info(original[3:], True)}
变卦: 上{self.get_wuxing_info(changed[:3], True)} 下{self.get_wuxing_info(changed[3:], True)}
互卦: 上{self.get_wuxing_info(mutual[:3], True)} 下{self.get_wuxing_info(mutual[3:], True)}
"""
        answer = self.ai_interpreter_session.send(hexagram_info, *args, **kwargs)
        result = DivinationComment(
            question=question,
            original=original,
            mutual=mutual,
            changed=changed,
            description=answer,
            metadata={"type": self._type}
        )
        return result
    
@Handler(IttrType.ITEM)
class ItemFoundHandler(BaseHandler):
    """ 寻物占卜处理器 """
    def __init__(self, handler: AIHandler) -> None:
        super().__init__(handler, IttrType.ITEM)

    def get_div_type(self) -> IttrType:
        return self._type
    
    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key
    
    def get_location_of_hexagram(self, hexagram: hexagramsType) -> tuple[tuple[str, str], tuple[str, str]]:
        upper = hexagram[:3]
        lower = hexagram[3:]
        upper_hexagram_name = HEXAGRAM_TO_STR[upper]
        lower_hexagram_name = HEXAGRAM_TO_STR[lower]
        # 先天和后天
        # 先天个人和地理方位
        self_location_first = INHERENT_HEXGRAM[upper_hexagram_name]
        geo_location_first = INHERENT_HEXGRAM[lower_hexagram_name]
        # 后天个人和地理方位
        self_location_second = ACQUIRED_HEXGRAM[upper_hexagram_name]
        geo_location_second = ACQUIRED_HEXGRAM[lower_hexagram_name]
        return (self_location_first, geo_location_first), (self_location_second, geo_location_second)
    
    def __call__(self, div_result: DivinationResult, *args, **kwargs) -> Optional[DivinationComment | str]:
        return self.handle(div_result, *args, **kwargs)
    
    def handle(self, div_result: DivinationResult, question: DivinationQuestion, *args, **kwargs) -> Optional[DivinationComment | str]:
        """
        解卦
        """
        original = div_result.original # 只用取本卦就好
        # 首先是个人方位
        location = self.get_location_of_hexagram(original)
        self_location_first = location[0][0]
        geo_location_first = location[0][1]
        self_location_second = location[1][0]
        geo_location_second = location[1][1]
        # 寻物占卜
        hexagram_info = f"""
        太卜大人，帮我解一下卦象并推测物品在哪，谢谢，占算的问题是 "{question}"，结果如下：
卦象: 上{HEXAGRAM_TO_STR[original[:3]]}|下{HEXAGRAM_TO_STR[original[3:]]},
先天方位: \n
个人: {self_location_first}, 地理: {geo_location_first}
后天方位: \n
个人: {self_location_second}, 地理: {geo_location_second}
"""
        answer = self.ai_interpreter_session.send(hexagram_info, *args, **kwargs)
        result = DivinationComment(
            question=question,
            original=original,
            mutual=div_result.mutual,
            changed=div_result.changed,
            description=answer,
            metadata={"type": self._type}
        )
        return result
    
@Handler(IttrType.ANOTHER)
class AnotherHandler(BaseHandler):
    """ 其他占卜处理器 """
    def __init__(self, handler: AIHandler) -> None:
        super().__init__(handler, IttrType.ANOTHER)

    def get_div_type(self) -> IttrType:
        return self._type
    
    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key
    
    def __call__(self, div_result: DivinationResult, *args, **kwargs) -> Optional[DivinationComment | str]:
        return self.handle(div_result, *args, **kwargs)
    
    def get_64_hexagram(self, hexagram: hexagramsType) -> str:
        """
        获取卦象的类型
        """
        try:
            return HEXAGRAMS_64_TO_NAME[hexagram]
        except KeyError:
            return "卦象还未被收录"
        
    def get_wuxing_info(self, hexagram: hexagramType, return_wuxing: bool = False) -> Union[dict[str, str], str]:
        """
        获取卦象的五行属性信息 (也是卦象相生相克的信息)
        如果 return_key 为 True, 则返回五行属性
        """
        try:
            hexagram_name = self.get_name_of_hexagram(hexagram)
            wuxing = HEXGRAM_TO_WUXING[hexagram_name]
            hexagram_wuxing_info = WUXING[wuxing]
            # 如果 return_key 为 True, 则返回五行属性的键值
            if return_wuxing:
                return wuxing
            else:
                return hexagram_wuxing_info
        except KeyError:
            return "未知五行属性或卦象"
    
    def handle(self, div_result: DivinationResult, question: DivinationQuestion, *args, **kwargs) -> Optional[DivinationComment | str]:
        """
        解卦
        """
        original = div_result.original
        mutual = div_result.mutual
        changed = div_result.changed
        orig_64 = self.get_64_hexagram(original)
        mutual_64 = self.get_64_hexagram(mutual)
        changed_64 = self.get_64_hexagram(changed)
        hexagram_info = f"""
        太卜大人，帮我解一下卦，谢谢，占算的人的问题是 "{question}"，下面是他占卜的结果：
本卦: {orig_64}
变卦: {changed_64}
互卦: {mutual_64}
五行属性: \n
本卦: 上{self.get_wuxing_info(original[:3], True)} 下{self.get_wuxing_info(original[3:], True)}
变卦: 上{self.get_wuxing_info(changed[:3], True)} 下{self.get_wuxing_info(changed[3:], True)}
互卦: 上{self.get_wuxing_info(mutual[:3], True)} 下{self.get_wuxing_info(mutual[3:], True)}
"""
        answer = self.ai_interpreter_session.send(hexagram_info, *args, **kwargs)
        result = DivinationComment(
            question=question,
            original=original,
            mutual=mutual,
            changed=changed,
            description=answer,
            metadata={"type": self._type}
        )
        return result