""" 画像群をまとめて回転する
"""
from typing import Any, List, Dict, Optional, Tuple
from pathlib import Path
from argparse import ArgumentParser
import logging
import sys

import tqdm
import numpy as np
import cv2

import _add_path
from imgtools import path_functions
from imgtools import utils


str2rotate_code:Dict[str, Any] = {
    "r90":cv2.ROTATE_90_CLOCKWISE,
    "l90":cv2.ROTATE_90_COUNTERCLOCKWISE,
    "reverse":cv2.ROTATE_180
}

def argparse() -> Dict[str, Any]:
    parser:ArgumentParser = ArgumentParser(description=__doc__)

    parser.add_argument("img_dir", type=str, help="img dir")
    parser.add_argument("--out_dir", type=str, default="None", help="default is <img_dir>_rotated")
    parser.add_argument("--rotate", type=str, choices=["r90", "l90", "reverse"], default="l90", 
                        help="Rorate option. Option is right 90 or left 90 or reverse. Default is l90")
    parser.add_argument("--y", action="store_true", help="skip ask process")

    return vars(parser.parse_args())


def main(*args, **kwargs):
    # show kwargs
    utils.show_kwargs(**kwargs)

    # parse
    src_dir:Path = parse_src_dir(kwargs["img_dir"], **locals())
    out_dir:Path = parse_out_dir(kwargs["out_dir"], **locals())
    rotate:str = kwargs["rotate"]

    # search img paths
    img_paths:List[Path] = path_functions.search_img_paths(src_dir, [".jpg", ".png"])

    # ask user continue program
    is_skip_ask:bool = kwargs["y"]
    if not is_skip_ask:
        ask_start(**locals())

    # make out dir
    out_dir.mkdir(exist_ok=True)

    # rotate loop
    for img_path in tqdm.tqdm(img_paths, desc="rotate img"):
        # load img
        img:Optional[np.ndarray] = load_img(img_path)
        if img is None:
            continue
        # rotate
        img = rotate_img(img, rotate)
        # save img
        save_img(img, img_path, out_dir, 100)


def parse_src_dir(path:str, **kwargs) -> Path:
    path_:Path = Path(path)
    utils.check_is_valid_dir(path_)
    return path_


def parse_out_dir(path:str, **kwargs) -> Path:
    is_use_default_dir:bool = path == "None"
    if is_use_default_dir:
        path_:Path = Path(f"{Path(kwargs['src_dir']).absolute()}_rotated")
    else:
        path_ = Path(path)
    utils.check_is_valid_dir(path_.parent)
    return path_


def ask_start(*args, **kwargs):
    num_imgs:int = len(kwargs['img_paths'])
    rotate_str:str = kwargs["rotate"]
    print(f" start rotate {num_imgs} imgs to {rotate_str} ?(y/n) >>", end="")
    input_:str = input()
    if input_ not in ["y", "Y", "Yes", "yes"]:
        sys.exit(0)


def load_img(path:Path) -> Optional[np.ndarray]:
    try:
        img:np.ndarray = cv2.imread(str(path))
    except Exception as e:
        logging.warning(f"skip read img from {path}, because can't read img" )
        return None
    return img


def save_img(img:np.ndarray, src_img_path:Path, out_dir:Path, quality:int):
    if src_img_path.suffix == ".png":
        save_as_png(img, src_img_path.stem, out_dir)
    elif src_img_path.suffix == ".jpg":
        save_as_jpg(img, src_img_path.stem, out_dir, quality)
    else:
        pass


def save_as_jpg(img:np.ndarray, out_file_name:str, out_dir:Path, quality:int=100):
    assert 0 <= quality <= 100, "quality is 0 < x < 100"
    out_path:Path = out_dir.joinpath(f"{out_file_name}.jpg")
    cv2.imwrite(str(out_path), img, params=[cv2.IMWRITE_JPEG_QUALITY, quality])


def save_as_png(img:np.ndarray, out_file_name:str, out_dir:Path):
    out_path:Path = out_dir.joinpath(f"{out_file_name}.png")
    cv2.imwrite(str(out_path), img)


def rotate_img(img:np.ndarray, rotate_str:str) -> np.ndarray:
    return cv2.rotate(img, str2rotate_code[rotate_str])


if __name__ == "__main__":
    cli_args:Dict[str, Any] = argparse()
    main(**cli_args)
