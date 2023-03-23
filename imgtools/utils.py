from typing import Any,Union
from pathlib import Path


def can_cvt_int(any:Any) -> bool:
    try:
        int(round(float(any), 0))
        return True
    except:
        return False


def check_can_cvt_int(any:Any):
    assert can_cvt_int(any), f"Can't convrt {any} to int"


def is_positive(num:int) -> bool:
    return True if num > 0 else False


def check_is_positive(num:int):
    assert can_cvt_int(num), f"{num} isn't positive"


def check_is_valid_path(path:Union[str, Path]):
    path_:Path = Path(path)
    assert path_.exists(), f"Not Found {Path}"


def check_is_valid_dir(path:Union[str, Path]):
    path_:Path = Path(path)
    check_is_valid_path(path_)
    assert path_.is_dir(), f"{path_} is not directory"


def check_is_valid_file(path:Union[str, Path]):
    path_:Path = Path(path)
    check_is_valid_path(path_)
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
