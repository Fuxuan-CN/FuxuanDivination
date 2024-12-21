
from Fuxuan import TimeDivination
from Fuxuan import Interpretation , DivType

# build exe file command:
# pyinstaller -F --onefile --version=resource/version.txt --icon=resource/icon.ico FuxuanDivination.py

if __name__ == '__main__':
    # 时间占卜
    divinator = TimeDivination()
    ittr = Interpretation(api_key="your_api_key") # 为了使用ZhipuAI的SDK，需要先申请API Key
    question = input("请输入问题：")
    result , hexagram_string = divinator.run(question=question)
    print(hexagram_string)
    resp = ittr.interpret(div_result=result,div_type=DivType.LUCK, question=question, output_to_file=True)
    print(resp)
