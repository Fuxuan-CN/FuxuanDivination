
from Fuxuan import TimeDivination
from Fuxuan import Interpretation

# build exe file command:
# pyinstaller -F --version-file resources/version.txt FuxuanDivination.py -i resources/icon.ico

if __name__ == '__main__':
    # 时间占卜
    divinator = TimeDivination()
    ittr = Interpretation()
    question = input("请输入问题：")
    result , div_result_string = divinator.run(question=question)
    ittr.interpret(div_result=result, output_to_console=True)
