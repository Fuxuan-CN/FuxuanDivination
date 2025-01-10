
from dataclasses import dataclass
from ._type import hexagramsType
from ._question import DivinationQuestion

@dataclass
class DivinationResult:
    """占卜结果"""
    original: hexagramsType
    mutual: hexagramsType
    changed: hexagramsType

@dataclass
class DivinationComment:
    """ 卦象解读 """
    question: DivinationQuestion
    original: hexagramsType | None
    mutual: hexagramsType | None
    changed: hexagramsType | None
    description: str # 解读
    metadata: dict # 其他信息

    def __str__(self) -> str:
        information = \
        f"""
问题: {self.question.content} \n
本卦: {self.original}
互卦: {self.mutual}
变卦: {self.changed} \n
=============== \n
解读: {self.description} \n
额外的信息: {self.metadata} \n
"""
        return information