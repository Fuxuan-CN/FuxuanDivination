
from Fuxuan import CalculateEightChar
from datetime import datetime

# build exe file command:
# pyinstaller -F --version-file resources/version.txt FuxuanDivination.py -i resources/icon.ico

if __name__ == '__main__':
    birthday = datetime(2007, 10, 18, 11, 30, 0)
    eight_char = CalculateEightChar.get_eight_char(birthday)
    print(eight_char)