
import os
import shutil

def clean_pycache():
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            print(f"Removed __pycache__ folder in {root}")

def pyinstaller_build():
    cmd = "pyinstaller -F --onefile --version-file=resources/version.txt --icon=resources/icon.ico FuxuanDivination.py"
    os.system(cmd)
    print("Pyinstaller build completed")
    print("Cleaning __pycache__ folders...")
    clean_pycache()
    print("Cleaned __pycache__ folders")

if __name__ == '__main__':
    pyinstaller_build()