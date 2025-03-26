from typing import Union, Optional
from pathlib import Path

import magic
import re


def get_resolution_png(path: Union[str, Path]):
    t: str = magic.from_file(str(path))
    matched: Optional[re.Match[str]] = re.search('(\\d+) x (\\d+)', t)
    assert matched is not None
    x = matched.groups()
    wsize: int = int(x[0])
    hsize: int = int(x[1])
    return wsize, hsize


def get_resolution_jpg(path: Union[str, Path]):
    t: str = magic.from_file(str(path))
    matched = re.findall('(\\d+)x(\\d+)', t)
    assert matched is not None
    x = matched[-1]
    wsize: int = int(x[0])
    hsize: int = int(x[1])
    return wsize, hsize
