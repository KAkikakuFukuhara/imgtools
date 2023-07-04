from typing import Optional, Any, Dict, List
from pathlib import Path
from argparse import ArgumentParser
import copy
import time
import shutil

import numpy as np
import cv2
import tqdm

import _add_path
from imgtools import path_functions, utils, img_functions

sift:Optional[Any] = None # cv2.SIFT
bf:Optional[Any] = None # cv2.BFMatcher


def argparse() -> Dict[str, Any]:
    parser:ArgumentParser = ArgumentParser(description=__doc__)

    parser.add_argument("img_dir", type=str, help="img dir")
    # parser.add_argument("thresh", type=int, help="img matching threshold")


    return vars(parser.parse_args())


def main(*args, **kwargs):
    # show kwargs
    utils.show_kwargs(**kwargs)

    # parse
    src_dir:Path = Path(kwargs["img_dir"])
    # thresh:int = kwargs['thresh']

    # search img paths
    img_paths:List[Path] = path_functions.search_img_paths(src_dir, [".jpg", ".png"])
    img_paths.sort()
    # img_paths = img_paths[:30]

    sift = cv2.SIFT_create()
    kpts = []
    dess = []
    for img_path in tqdm.tqdm(img_paths):
        src_img = cv2.imread(str(img_path))
        gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        kpt, des = sift.detectAndCompute(gray_img, None)
        kpts.append(kpt)
        dess.append(des)

    dsc_img_paths = extract_non_duplication(img_paths, dess, 2000)
    for img_path in dsc_img_paths:
        img = cv2.imread(str(img_path))
        show_img(img)

    save_imgs(dsc_img_paths)


def extract_non_duplication(img_paths:List[Path], dess:list, thresh:int=3000):
    src_img_paths = copy.copy(img_paths)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    src_dess = copy.copy(dess)
    dsc_img_paths = []
    start_time = time.time()
    while(len(src_img_paths) > 1):
        elapd_time = time.time() - start_time
        print(f"elapd:{elapd_time:4.3f}残り枚数:{len(src_img_paths)}")
        dsc_img_paths.append(src_img_paths.pop(0))
        curr_des = src_dess.pop(0)
        num_matches = []
        for des in src_dess:
            num_matches.append(len(bf.match(curr_des, des)))
        for idx in range(len(num_matches))[::-1]:
            if num_matches[idx] > thresh:
                src_img_paths.pop(idx)
                src_dess.pop(idx)
    return dsc_img_paths


def show_img(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_imgs(imgs):
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    for img in imgs:
        out_flie = out_dir.joinpath(img.name)
        shutil.copy(img, out_flie)

if __name__ == "__main__":
    main(**argparse())