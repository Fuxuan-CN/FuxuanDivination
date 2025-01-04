
class Num:
    """占卜数字类表示"""
    def __init__(self,
        first_num: int,
        second_num: int,
        third_num: int
    ) -> None:
        self.first_num = first_num
        self.second_num = second_num
        self.third_num = third_num

    def __str__(self) -> str:
        return f"first: {self.first_num}, second: {self.second_num}, third: {self.third_num}"
    
    def __repr__(self) -> str:
        return f"Num({self.first_num}, {self.second_num}, {self.third_num})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Num):
            return False
        return self.first_num == other.first_num and self.second_num == other.second_num and self.third_num == other.third_num
    
    def __hash__(self) -> int:
        return hash((self.first_num, self.second_num, self.third_num))