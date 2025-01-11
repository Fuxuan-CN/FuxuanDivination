
from fuxuan.example import main

# build executable using pyinstaller:
# pyinstaller -F --onefile --version-file=resources/version.txt --icon=resources/icon.ico FuxuanDivination.py
# build executable using nuitka:
# nuitka --standalone --windows-icon-from-ico=resources/icon.ico --version-file=resources/version.txt FuxuanDivination.py

if __name__ == '__main__':
    main()