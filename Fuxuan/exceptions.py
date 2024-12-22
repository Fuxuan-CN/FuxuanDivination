

# 定义一些库的异常类

class FuxuanException(Exception):
    """
    此库异常的基类
    """
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

class ArgumentRequired(FuxuanException):
    """
    参数缺失异常
    """
    def __init__(self, message: str):
        super().__init__(1000, message)

class ErrorUsage(FuxuanException):
    """ 不正确的使用方式 """
    def __init__(self, message: str):
        super().__init__(1001, message)

class DivinationHandlerError(FuxuanException):
    """ 处理器错误 """
    def __init__(self, message: str):
        super().__init__(1002, message)

class DivinationHandlerNotFound(DivinationHandlerError):
    """ 处理器未找到 """
    def __init__(self, message: str):
        super().__init__(message)

class DivinationError(FuxuanException):
    """ 其他错误 """
    def __init__(self, message: str):
        super().__init__(1003, message)