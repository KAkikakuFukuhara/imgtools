from typing import Union, List
from pathlib import Path

JPEG_SUFFIX:str = ".jpg"
PNG_SUFFIX:str = ".png"

def check_path(path:Union[str, Path]):
    path_:Path = Path(path)
    assert path_.exists(), f"Not Found {path_}"


def search_img_paths(dir:Union[str, Path], suffixes:List[str]):
    dir_:Path = Path(dir)
    check_path(dir_)

    assert len(suffixes) > 0, "Non elements in suffixes"
    for suf in suffixes:
        assert isinstance(suf, str), "Suffixes include non str"

    suffixes_:List[str] = suffixes + [suf.upper() for suf in suffixes] # [".jpg"] to [".jpg", ".JPG"]
    img_paths:List[Path] = [path for suf in suffixes_ for path in dir_.glob(f"*{suf}")]
    assert img_paths, f"Not Found file that {suffixes} in {dir_}"

    return img_paths
