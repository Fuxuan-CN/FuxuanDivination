
import os
import shutil
import argparse

def clean_pycache():
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            print(f"Removed __pycache__ folder in {root}")

def pyinstaller_build():
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Please install it using pip.")
        return
    cmd = "pyinstaller -F --onefile --version-file=resources/version.txt --icon=resources/icon.ico FuxuanDivination.py"
    os.system(cmd)
    print("Pyinstaller build completed")
    print("Cleaning __pycache__ folders...")
    clean_pycache()
    print("Cleaned __pycache__ folders")

def main():
    parser = argparse.ArgumentParser(description='构建Divination.exe的工具')
    parser.add_argument('-b', '--build', action='store_true', help='构建Divination.exe')
    parser.add_argument('-c', '--clean', action='store_true', help='清理__pycache__文件夹')
    args = parser.parse_args()
    if args.build:
        pyinstaller_build()
    elif args.clean:
        clean_pycache()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()