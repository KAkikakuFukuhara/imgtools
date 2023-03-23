from typing import Union
from pathlib import Path


def check_path_exists(path:Union[str, Path]):
    path_:Path = Path(path)
    assert path_.exists(), f"Not Found {Path}"


def check_dir(path:Union[str, Path]):
    path_:Path = Path(path)
    check_path_exists(path_)
    assert path_.is_dir(), f"{path_} is not directory"


def check_file(path:Union[str, Path]):
    path_:Path = Path(path)
    check_path_exists(path_)
    assert path_.is_file(), f"{path_} is not file"


def show_kwargs(*args, **kwargs):
    all_txt:str = ""
    fin_txt:str = ""
    all_txt += "┌ args ─────────────\n"
    all_txt += "│\n"
    fin_txt += "│\n"
    fin_txt += "└────────────────"
    for k, v in kwargs.items():
        all_txt += f"│ - {k}\n"
        all_txt += f"│ \t - {v}\n"
    all_txt += fin_txt
    print(all_txt)