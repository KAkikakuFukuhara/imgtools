"""
png画像群をjpg画像群に変換するプログラム
"""
from typing import Any, List, Dict, Optional
from pathlib import Path
from argparse import ArgumentParser
import logging

import tqdm
import numpy as np
import cv2

import _add_path
from imgtools import path_functions

def argparse() -> Dict[str, Any]:
    parser:ArgumentParser = ArgumentParser(description=__doc__)

    parser.add_argument("png_dir", type=str, help="png dir")
    parser.add_argument("--out_dir", type=str, default="None", help="default is <PNG_DIR>_jpg")
    parser.add_argument("-q", "--quality", type=int, default=100, help="compression ratio. default is 100")

    return vars(parser.parse_args())


def main(*args, **kwargs):
    src_dir:Path = Path(kwargs["png_dir"])
    img_paths:List[Path] = path_functions.search_img_paths(src_dir, [".png"])

    if kwargs["out_dir"] == "None":
        out_dir:Path = Path(f"{src_dir}_jpg")
    else:
        out_dir = Path(kwargs["out_dir"])
    assert out_dir.parent.exists()
    out_dir.mkdir(exist_ok=True)

    print(f"png to jpg and save for {out_dir}")
    for img_path in tqdm.tqdm(img_paths, desc="imgs"):
        img:Optional[np.ndarray] = load_img(img_path)
        if img is None:
            continue
        out_file_name:str = img_path.stem
        save_as_jpg(img, out_file_name, out_dir, kwargs["quality"])


def load_img(path:Path) -> Optional[np.ndarray]:
    try:
        img:np.ndarray = cv2.imread(str(path))
    except Exception as e:
        logging.warning(f"skip read img from {path}, because can't read img" )
        return None
    return img


def save_as_jpg(img:np.ndarray, out_file_name:str, out_dir:Path, quality:int=100):
    assert 0 < quality < 100, "quality is 0 < x < 100"
    out_path:Path = out_dir.joinpath(f"{out_file_name}.jpg")
    cv2.imwrite(str(out_path), img, params=[cv2.IMWRITE_JPEG_QUALITY, quality])


if __name__ == "__main__":
    cli_args:Dict[str, Any] = argparse()
    main(**cli_args)