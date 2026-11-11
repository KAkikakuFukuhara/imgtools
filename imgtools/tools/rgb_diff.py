""" rgb値の差分画像を表示する
"""
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Any

import cv2
import numpy as np

import _add_path
from imgtools import path_functions


DEFAULT_IMG_SHAPE = (270, 480, 3)


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
    parser.add_argument("--imgdir", type=str, default="NONE", help="imgdir")
    return parser


def main(*args, **kwargs):
    myargs = MyArgs(**kwargs)

    paths: list[Any]
    if myargs.is_debug:
        paths = [None]
    else:
        suffixes = [".jpg", ".png"]
        paths = path_functions.search_img_paths(myargs.imgdir, suffixes)

    imshow(paths)


class MyArgs:
    def __init__(self, *args, **kwargs):
        self.is_debug = self._parse_debug(**kwargs)
        self.imgdir = self._parse_imgdir(**kwargs)


    def _parse_debug(*args, **kwargs):
        is_debug = kwargs['debug']
        return is_debug


    def _parse_imgdir(self, *args, **kwargs):
        imgdir = Path(kwargs['imgdir'])
        if not self.is_debug:
            assert imgdir.exists()
            assert imgdir.is_dir()
        return imgdir


def imshow(paths: list[Optional[Path]]):
    cur_idx = 0
    pre_idx = -1
    num_all_img = len(paths)
    cv2.namedWindow("image")
    cv2.namedWindow("image2")
    cv2.namedWindow("image3")
    try:
        while(True):
            ### load img
            src_img = load_img(paths, cur_idx)
            pre_idx = cur_idx

            ### edit
            src_img = cv2.resize(src_img, DEFAULT_IMG_SHAPE[:2][::-1])
            img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
            img = channels_split_and_diff(img)
            img2 = cvt_binary_img(img, 0.5)
            ### imshow
            cv2.imshow("image", img)
            cv2.imshow("image2", src_img)
            cv2.imshow("image3", img2)
            key = cv2.waitKey(0) & 0xff

            ### key press command
            if key == ord('q'):
                break
            if key == ord('f'):
                if cur_idx < num_all_img -1:
                    cur_idx +=1
            if key == ord('d'):
                if cur_idx > 0:
                    cur_idx -=1
    finally:
        cv2.destroyAllWindows()


def load_img(paths: list[Optional[Path]], idx: int) -> np.ndarray:
    path: Optional[Path] = paths[idx]
    if isinstance(path, Path):
        img = cv2.imread(str(path))
    else:
        img = np.zeros(DEFAULT_IMG_SHAPE, np.uint8)
        img[100:200, 50:200, 0] = 150
        img[100:200, 150:300, 1] = 150
        img[100:200, 250:400, 2] = 150
    return img


def channels_split_and_diff(img: np.ndarray):
    """ RGB画像から各チャンネルを取り出して差分を取って結合する
    """
    img_r = img[:,:,0]
    img_g = img[:,:,1]
    img_b = img[:,:,2]
    img_r_g = diff_img(img_r, img_g)
    img_g_b = diff_img(img_g, img_b)
    img_b_r = diff_img(img_b, img_r)
    img_r_g_b = diff_img(img_r_g, img_g_b)
    img_g_b_r = diff_img(img_g_b, img_b_r)
    img_b_r_g = diff_img(img_b_r, img_r_g)

    img1 = np.concatenate([img_r, img_g, img_b], axis=1)
    img2 = np.concatenate([img_r_g, img_g_b, img_b_r], axis=1)
    img3 = np.concatenate([img_r_g_b, img_g_b_r, img_b_r_g], axis=1)

    dst_img = np.concatenate([img1, img2, img3], axis=0)
    return dst_img


def diff_img(img1: np.ndarray, img2: np.ndarray):
    dst_img = img1 - img2
    dst_img -= dst_img.min()
    dst_img = normalize(dst_img)
    return dst_img


def normalize(img: np.ndarray):
    img = (img / img.max()) * 255
    img = img.astype(np.uint8)
    return img


def cvt_binary_img(img: np.ndarray, thr:float=0.5):
    thr_value = int(img.max() * thr)
    dst_img = np.where(img > thr_value, 255, 0)
    return dst_img.astype(np.uint8)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))