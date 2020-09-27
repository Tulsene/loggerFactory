import os
import sys

def set_root_path() -> str:
    root_path = os.path.dirname(sys.argv[0])
    return f'{root_path}/' if root_path else ''

def create_dir_when_none(dir_name:str) -> bool:
    if not os.path.isdir(dir_name):
        print('hey')
        os.makedirs(dir_name)
        
        return False

    return True