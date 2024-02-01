''' 画像を合成する
'''
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path

import cv2
import numpy as np
import tqdm

import _add_path
from imgtools import path_functions as imgp
from imgtools import utils


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("dir1", type=str, help="dir1")
    parser.add_argument("dir2", type=str, help="dir2")
    parser.add_argument("-v", "--vertical", action="store_true", help="concat vertical flag")
    parser.add_argument("-o", "--out", type=str, default="./", help="outdir root path. Default is ./")

    return vars(parser.parse_args())


def main(*args, **kwargs):
    dir1 = Path(kwargs['dir1'])
    dir2 = Path(kwargs['dir2'])
    is_vertical: bool = kwargs['vertical']
    imgpaths1: list[Path] = imgp.search_img_paths(dir1, suffixes=["jpg", "png"])
    imgpaths2: list[Path] = imgp.search_img_paths(dir2, suffixes=["jpg", "png"])
    imgpaths1.sort()
    imgpaths2.sort()

    outdir = Path(kwargs['out']).joinpath("concated")
    utils.check_is_valid_dir(outdir.absolute().parent)
    outdir.mkdir(exist_ok=True)
    print(f"save to {outdir.absolute()}")

    min_num_imgpaths = min([len(imgpaths1), len(imgpaths2)])
    print(f"Num Imgs, MIN:{min_num_imgpaths}, DIR1:{len(imgpaths1)}, DIR2:{len(imgpaths2)}")
    for idx in tqdm.tqdm(range(min_num_imgpaths), desc="concat and write"):
        # concat img h or v
        img1: np.ndarray = cv2.imread(str(imgpaths1[idx])) # type:ignore
        img2: np.ndarray = cv2.imread(str(imgpaths2[idx])) # type:ignore
        concated_img: np.ndarray = concat_imgs(img1, img2, is_vertical)
        # save output file
        out_file = outdir.joinpath(f"{imgpaths1[idx].stem}.png")
        cv2.imwrite(str(out_file), concated_img) # type:ignore


def concat_imgs(img1: np.ndarray, img2: np.ndarray, is_vertical: bool) -> np.ndarray:
    """ 2枚の画像を任意の方向に連結される。
        画像サイズが異なる場合、小さい方の画像にゼロパディングを付加して連結させる
    """
    shapes: np.ndarray = np.array([list(img1.shape), list(img2.shape)])
    if is_vertical: # concat vertical
        max_wsize: int = max(shapes[:, 1])
        canvas1: np.ndarray = np.zeros((img1.shape[0], max_wsize, 3), np.uint8)
        canvas1[:img1.shape[0], :img1.shape[1], :] = img1
        canvas2: np.ndarray = np.zeros((img2.shape[0], max_wsize, 3), np.uint8)
        canvas2[:img2.shape[0], :img2.shape[1], :] = img2
        concated_img: np.ndarray = np.concatenate([canvas1, canvas2], axis=0)
    else: # concat horizon
        max_hsize: int = max(shapes[:, 0])
        canvas1: np.ndarray = np.zeros((max_hsize, img1.shape[1], 3), np.uint8)
        canvas1[:img1.shape[0], :img1.shape[1], :] = img1
        canvas2: np.ndarray = np.zeros((max_hsize, img2.shape[1], 3), np.uint8)
        canvas2[:img2.shape[0], :img2.shape[1], :] = img2
        concated_img: np.ndarray = np.concatenate([canvas1, canvas2], axis=1)
    return concated_img

if __name__ == "__main__":
    main(**parse_args())