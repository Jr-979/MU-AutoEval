import subprocess
from evaluation import main

if __name__ == '__main__':
    try:
        main()
    
    except ModuleNotFoundError:
        subprocess.check_call(["pip","install","-r","requirement.txt"])
        main()