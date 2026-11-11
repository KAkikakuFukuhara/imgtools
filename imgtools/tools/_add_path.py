import sys
from pathlib import Path

_FILE_DIR:Path = Path(__file__).absolute().parent
ROOT_DIR:Path = _FILE_DIR.parent

def add_path():
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))


add_path()

if __name__ == "__main__":
    # check sys path
    import pprint
    pprint.pprint(sys.path)