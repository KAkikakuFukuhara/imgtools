""" RGB画像をGRAY画像に変換
"""
from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser

import cv2
import numpy as np
import tqdm

import _add_path
from imgtools import path_functions


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("img", type=str, help="img path")
    return parser


def main(*args, **kwargs):
    # argument process
    src_path = Path(kwargs["img"])
    assert src_path.exists()

    # get img paths
    img_paths: list[Path]
    if src_path.is_file():
        img_paths = [src_path]
    else:
        suffixes = [".jpg", ".png"]
        img_paths = path_functions.search_img_paths(src_path, suffixes)

    # main loop
    assert len(img_paths) > 0, f"Not Found img in {src_path}"
    out_dir = Path(f"{img_paths[0].parent}_gray")
    out_dir.mkdir(exist_ok=True)
    miss_list:list[Path] = []
    for ip in tqdm.tqdm(img_paths, desc="cvt2rgb"):
        is_success: bool = process_single_img(ip, out_dir)
        if not is_success:
            miss_list.append(ip)

    # show error img 
    if len(miss_list)>0:
        print("error path")
        print(miss_list)

    print("Finish!!")


def process_single_img(img_path: Path, out_dir:Path):
    """ load img. convert rgb to gray. write img.
    """
    try:
        src_img = cv2.imread(str(img_path)) #type:ignore
        # print(f"Loaded img from '{img_path}")

        dst_img = cvt_color_BGR2GRAY(src_img)
        # print("Converted img color BGR to GRAY")

        dst_img_path = out_dir.joinpath(f"{img_path.stem}_gray.png")
        cv2.imwrite(str(dst_img_path), dst_img) #type:ignore
        # print(f"Save img to '{dst_img_path}'")
    except Exception as e:
        print(e)
        return False
    else:
        return True


def cvt_color_BGR2GRAY(src_img: np.ndarray) -> np.ndarray:
    """ convert rgb2gray
    """
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY) #type:ignore
    dst_img = np.zeros(src_img.shape, src_img.dtype)
    dst_img[:, :, 0] = gray_img
    dst_img[:, :, 1] = gray_img
    dst_img[:, :, 2] = gray_img
    return dst_img


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))