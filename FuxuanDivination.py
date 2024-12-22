
from Fuxuan import Num, Divinator
from Fuxuan import Interpretation, DivinationType , IttrType
import os

# build exe file command:
# pyinstaller -F --onefile --version-file=resources/version.txt --icon=resources/icon.ico FuxuanDivination.py

if __name__ == '__main__':
    # 时间占卜
    divinator = Divinator()
    question = input("请输入问题：").strip()
    if not os.path.exists("api_key.key"):
       api_key = input("请输入API Key：").strip()
       with open("api_key.key", "w") as key_file:
           key_file.write(api_key)
    else:
       with open("api_key.key") as key_file:
           api_key = key_file.read().strip()
    div_t = input("请输入占卜类型(luck/item)：").strip()
    div_method = input("请输入占卜方法(time/num)：").strip()
    ittr = Interpretation(api_key)
    if div_method not in ['time', 'num']:
        print("占卜方法错误，请重新输入！")
        exit(1)
    if div_t not in ['luck', 'item']:
        print("占卜类型错误，请重新输入！")
        exit(1)
    IttrType.LUCK if div_t == 'luck' else IttrType.ITEM
    
    if div_method == "num":
        number1 = int(input("请输入第一个数字：").strip())
        number2 = int(input("请输入第二个数字：").strip())
        number3 = int(input("请输入第三个数字：").strip())
        num = Num(number1, number2, number3)
        result, hexagram_readable = divinator.run(question, DivinationType.NUMBER, num)
    elif div_method == "time":
        result, hexagram_readable = divinator.run(question, DivinationType.TIME)
    ittr.interpret(result, div_t, question, output_to_file=True) #type: ignore
