from ...utils import NUM_TO_HEXGRAM_STR , HEXAGRAM_DESCRIPTION_STR , YANG , YIN, NOW, ZHI_TO_TIME, ZHI_NUM, HEXGRAM_DESCRIPTION, DIZHI , CalculateEightChar
from ...interface import DivinationHandlerAble
from ...model import hexagramType , hexagramsType , DivinationResult, DivinationType, DivinationQuestion
from .handler_data import Num
from lunarcalendar import Converter, Solar, DateNotExist
import datetime
from functools import wraps

DIVINATION_HANDLER: dict[DivinationType, type[DivinationHandlerAble]] = {}
""" 注册的占卜处理器字典 """

def DivinationHandler(div_type: DivinationType):
    """
    注册占卜处理器的装饰器
    """
    @wraps(DivinationHandler)
    def wrapper(cls):
        DIVINATION_HANDLER[div_type] = cls
        return cls
    return wrapper

@DivinationHandler(DivinationType.NUMBER)
class NumDivination(DivinationHandlerAble):
    """数字占卜类"""
    def __init__(self, num: Num) -> None:
        self.num = num

    def get_upper_hexagram(self) -> hexagramType:
        """获取上卦"""
        r_num = self.num.first_num % 8
        if r_num == 0:
            r_num = 8
        hexagram_str = NUM_TO_HEXGRAM_STR[r_num]
        hexagram = HEXAGRAM_DESCRIPTION_STR[hexagram_str]
        return hexagram
    
    def get_lower_hexagram(self) -> hexagramType:
        """获取下卦"""
        r_num = self.num.second_num % 8
        if r_num == 0:
            r_num = 8
        hexagram_str = NUM_TO_HEXGRAM_STR[r_num]
        hexagram = HEXAGRAM_DESCRIPTION_STR[hexagram_str]
        return hexagram
    
    def change_yao(self, yao: str) -> str:
        """变爻"""
        if yao == YANG:
            return YIN
        else:
            return YANG
    
    def get_original_hexagram(self) -> tuple[hexagramsType, int]:
        upper = self.get_upper_hexagram()
        lower = self.get_lower_hexagram()
        orig_hexagram = upper + lower
        changed = self.num.third_num % 6 # 爻以六除余
        return orig_hexagram , changed
    
    def get_mutual_hexagram(self) -> hexagramsType:
        """获取互卦"""
        orig_hexagram, _ = self.get_original_hexagram()
        mutual_upper = (orig_hexagram[3], orig_hexagram[2], orig_hexagram[1]) # 取本卦的 3, 4, 5 为上卦
        mutual_lower = (orig_hexagram[4], orig_hexagram[3], orig_hexagram[2]) # 取本卦的 2, 3, 4 为下卦
        mutual_hexagram = mutual_upper + mutual_lower
        return mutual_hexagram
    
    def get_changed_hexagram(self) -> hexagramsType:
        """获取变卦"""
        orig_hexagram, changed = self.get_original_hexagram()
        # 从下往上看, 先倒序排列
        hexagram = [hexagram for hexagram in reversed(orig_hexagram)]
        _changed = changed - 1 # 因为索引从0开始, 所以要减1
        hexagram[_changed] = self.change_yao(hexagram[_changed])
        changed_hexagram = tuple(reversed(hexagram)) # 再反转回来，并转为元组
        return changed_hexagram # type: ignore
    
    def build_hexagram(self) -> DivinationResult:
        """构建卦象"""
        orig_hexagram, _ = self.get_original_hexagram()
        mutual_hexagram = self.get_mutual_hexagram()
        changed_hexagram = self.get_changed_hexagram()
        result = DivinationResult(original=orig_hexagram, mutual=mutual_hexagram, changed=changed_hexagram)
        return result
        
    
    def handle(self, question: DivinationQuestion) -> tuple[DivinationResult, str]:
        """运行占卜"""
        result = ""
        hexagram = self.build_hexagram()
        result +="对于你的问题,卦象情况如下:\n"
        result += f"本卦: \n{hexagram.original}\n"
        result += f"互卦: \n{hexagram.mutual}\n"
        result += f"变卦: \n{hexagram.changed}\n"
        return hexagram , result

@DivinationHandler(DivinationType.TIME)
class TimeDivination(DivinationHandlerAble):

    def get_lunar_day_and_month(self) -> tuple[int, int]:
        """
        获取当前农历日期
        """
        try:
            # 获取当前公历日期
            solar_date = Solar(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            
            # 转换为农历日期
            lunar_date = Converter.Solar2Lunar(solar_date)
            
            lunar_month = lunar_date.month
            lunar_day = lunar_date.day

            return lunar_month, lunar_day
        except DateNotExist:
            return 0, 0
        

    def get_year_zhi(self) -> str:
        """
        根据公历年份获取对应的地支
        """
        # 1984年是甲子年，用当前年份减去1984，然后取余数确定地支
        year = NOW.year
        index = (year - 1984) % 12
        return DIZHI[index]
    
    def get_current_zhi_and_num(self) -> tuple[str, int]:
        """
        获取当前的时辰和时辰数
        """
        current_hour = NOW.hour
        for zhi, (start, end, day_zhi_num) in ZHI_TO_TIME.items():
            if start <= current_hour < end:
                return zhi , day_zhi_num
            # 处理子时（23:00 - 01:00）和跨越日期分界的情况
            if zhi == "子时" and (current_hour >= 23 or current_hour < 1):
                return zhi , day_zhi_num
        return "未知时辰" , 0
    
    def get_current_zhi_and_num_by_lunar(self) -> tuple[str, int]:
        """
        获取当前农历日期的地支
        """
        year_zhi = self.get_year_zhi()
        # 农历日期转阳历日期
        return year_zhi, ZHI_NUM[year_zhi]
    

    def get_upper_hexgram(self) -> hexagramType:
        """
        获取上卦
        算法为:
        (年 + 农历月 + 农历日) / 8 = result ... 余数确定 (卦以八除)
        """
        year_zhi = self.get_year_zhi()
        ld_date = self.get_lunar_day_and_month()
        zhi_num = ZHI_NUM[year_zhi]
        remainder = (zhi_num + ld_date[0] + ld_date[1]) % 8
        if remainder == 0: # 坤卦
            return HEXGRAM_DESCRIPTION[8]
        else:
            return HEXGRAM_DESCRIPTION[remainder]

    def get_lower_hexagram(self) -> hexagramType:
        """
        获取下卦
        方法是 (年 + 农月 + 农日 + 时辰) % 8 ... 取余数确定卦象
        """
        _ , year_num = self.get_current_zhi_and_num_by_lunar()
        ld_date = self.get_lunar_day_and_month()
        now_zhi = self.get_current_zhi_and_num()
        # 获取余数
        remainder = (year_num + ld_date[0] + ld_date[1] + now_zhi[1]) % 8
        if remainder == 0: # 坤卦
            return HEXGRAM_DESCRIPTION[8]
        else:
           return HEXGRAM_DESCRIPTION[remainder]
    
    def get_changed_yao(self, yao: str) -> str:
        """
        根据当前爻的状态，返回反转后的爻
        """
        if yao == YANG:
            return YIN
        elif yao == YIN:
            return YANG
        return yao  # 如果传入的 yao 不是 YANG 或 YIN，就返回原样

    def get_changed_hexagram(self, hexagram: hexagramsType) -> hexagramsType:
        """
        根据当前的卦象，返回变卦后的卦象
        算法步骤:
        (年 + 农月 + 农日 + 时) / 6 = result ... 余数确定变卦象(爻以六除)
        """
        year_zhi, year_num = self.get_current_zhi_and_num_by_lunar()
        ld_date = self.get_lunar_day_and_month()
        now_zhi = self.get_current_zhi_and_num()
        # 获取余数
        remainder = (year_num + ld_date[0] + ld_date[1] + now_zhi[1]) % 6
        _changed_hexagram = list(reversed(hexagram)) # 先反转原卦，因为再易经中，卦象是从下往上看的
        _changed: int = remainder - 1 # 这个代表第几个爻变了
        _changed_hexagram[_changed] = self.get_changed_yao(_changed_hexagram[_changed])
        changed_hexagram = tuple(reversed(_changed_hexagram)) # 再反转回来
        return changed_hexagram # type: ignore
        

    def build_hexagram(self) -> DivinationResult:
        """
        构建卦象，包括本卦、互卦和变卦
        """
        # 本卦
        upper_hexagram = self.get_upper_hexgram()
        lower_hexagram = self.get_lower_hexagram()
        original_hexagram = upper_hexagram + lower_hexagram

        # 互卦 (取本卦的 345 做上卦, 234 做下卦)
        mutual_upper = (original_hexagram[3], original_hexagram[2], original_hexagram[1])
        mutual_lower = (original_hexagram[4], original_hexagram[3], original_hexagram[2])
        mutual_hexagram = mutual_upper + mutual_lower

        # 变卦
        changed_hexagram = self.get_changed_hexagram(original_hexagram)

        result = DivinationResult(original=original_hexagram, mutual=mutual_hexagram, changed=changed_hexagram)
        return result
    
    def handle(self, question: DivinationQuestion) -> tuple[DivinationResult, str]:
        """
        主程序入口
        """
        hexagram = self.build_hexagram()
        year_gan , year_zhi = CalculateEightChar.get_year(NOW.year)
        result = f"占卜时间: {NOW.strftime('%Y-%m-%d %H:%M:%S')}({year_gan}{year_zhi}年)({self.get_current_zhi_and_num()[0]})"
        result +=f"问题：{question.content}，占得卦象情况如下:\n"
        result += f"本卦: \n{hexagram.original}\n"
        result += f"互卦: \n{hexagram.mutual}\n"
        result += f"变卦: \n{hexagram.changed}\n"
        return hexagram , result