
import os
import shutil

def clean_pycache():
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            print(f"Removed __pycache__ folder in {root}")

if __name__ == '__main__':
    clean_pycache()