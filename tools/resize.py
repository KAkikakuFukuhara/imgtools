""" 画像群をまとめてリサイズする
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

def argparse() -> Dict[str, Any]:
    parser:ArgumentParser = ArgumentParser(description=__doc__)

    parser.add_argument("img_dir", type=str, help="img dir")
    parser.add_argument("--out_dir", type=str, default="None", help="default is <img_dir>_resized")
    parser.add_argument("--resolution", type=str, default="640x480",
                        help="Resize resolution. Format is WidthxHeight. \
                        If you keep aspect ratio, use WidthxAny or AnyorHeight")
    parser.add_argument("--y", action="store_true", help="skip ask process")


    return vars(parser.parse_args())


def main(*args, **kwargs):
    # show kwargs
    utils.show_kwargs(**kwargs)

    # parse
    src_dir:Path = parse_src_dir(kwargs["img_dir"], **locals())
    out_dir:Path = parse_out_dir(kwargs["out_dir"], **locals())
    resolution:str = parse_resolution(kwargs["resolution"], **locals())

    # search img paths
    img_paths:List[Path] = path_functions.search_img_paths(src_dir, [".jpg", ".png"])

    # ask user continue program
    is_skip_ask:bool = kwargs["y"]
    if not is_skip_ask:
        ask_start(**locals())


    # make out dir
    out_dir.mkdir(exist_ok=True)

    # resize loop
    for img_path in tqdm.tqdm(img_paths, desc="resize img"):
        # load img
        img:Optional[np.ndarray] = load_img(img_path)
        if img is None:
            continue
        # resize
        img = resize_img(img, resolution)
        # save img
        save_img(img, img_path, out_dir, 100)


def parse_src_dir(path:str, **kwargs) -> Path:
    path_:Path = Path(path)
    utils.check_is_valid_dir(path_)
    return path_


def parse_out_dir(path:str, **kwargs) -> Path:
    is_use_default_dir:bool = path == "None"
    if is_use_default_dir:
        path_:Path = Path(f"{kwargs['src_dir']}_resized")
    else:
        path_ = Path(path)
    utils.check_is_valid_dir(path_.parent)
    return path_


def parse_resolution(resolution:str, **kwargs):
    check_is_valid_resolution(resolution)
    return resolution


def ask_start(*args, **kwargs):
    num_imgs:int = len(kwargs['img_paths'])
    resolution:str = kwargs['resolution']
    print(f" start resize {num_imgs} imgs to WidthxHeight={resolution} ? (y/n) >> ", end="")
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


def check_is_valid_resolution(resolution:str):
    words:List[str] = resolution.split("x")
    assert len(words) == 2, f"Resotion should is WsizexHsize, but recive {resolution}"
    is_any_wsize:bool = words[0] in ["Any", "any"]
    is_any_hsize:bool = words[1] in ["Any", "any"]
    assert not is_any_wsize & is_any_hsize, f"only use Any is 1 element"

    if not is_any_wsize:
        utils.check_can_cvt_int(words[0])
        utils.check_is_positive(int(words[0]))
    if not is_any_hsize:
        utils.check_can_cvt_int(words[1])
        utils.check_is_positive(int(words[1]))


def resize_img(img:np.ndarray, resolution:str) -> np.ndarray:
    src_wsize:int
    src_hsize:int
    src_hsize, src_wsize = img.shape[:2]

    words:List[str] = resolution.split("x")
    is_any_wsize:bool = words[0] in ["Any", "any"]
    is_any_hsize:bool = words[1] in ["Any", "any"]
    if is_any_wsize:
        dsc_hsize:int = int(words[1])
        ratio:float = dsc_hsize / src_hsize
        dsc_wsize:int = int(round(src_wsize * ratio, 0))
    elif is_any_hsize:
        dsc_wsize:int = int(words[0])
        ratio:float = dsc_wsize / src_wsize
        dsc_hsize:int = int(round(src_hsize * ratio, 0))
    else:
        dsc_wsize:int = int(words[0])
        dsc_hsize:int = int(words[1])

    return cv2.resize(img, (dsc_wsize, dsc_hsize))


if __name__ == "__main__":
    cli_args:Dict[str, Any] = argparse()
    main(**cli_args)
