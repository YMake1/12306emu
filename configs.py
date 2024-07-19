import os

project_root = os.path.dirname(os.path.abspath(__file__))

cache_path = os.path.join(project_root, 'cache')

def ensure_path_exists(rootpath: str, finalpath: str):
    path = os.path.join(rootpath, finalpath)
    if os.path.isdir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    elif os.path.isfile(path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, 'w') as file:
            pass
    else:
        os.makedirs(path)