""" 画像群から前のフレームの似た画像を削除する。
"""
from typing import Any, List, Dict, Optional, Tuple
from pathlib import Path
from argparse import ArgumentParser
import logging
import sys
import shutil
import time
import copy

import tqdm
import numpy as np
import cv2

import _add_path
from imgtools import path_functions
from imgtools import utils
from imgtools import img_functions


def argparse() -> Dict[str, Any]:
    parser:ArgumentParser = ArgumentParser(description=__doc__)

    parser.add_argument("img_dir", type=str, help="img dir")
    parser.add_argument("--lt", type=int, default=200, help="laplacian threshold for bure detection")
    parser.add_argument("--st", type=int, default=2000, help="num descirpter threshold for delete similarity")
    parser.add_argument("--y", action="store_true", help="skip ask process")
    parser.add_argument("--debug", action="store_true")


    return vars(parser.parse_args())


def main(*args, **kwargs):
    # show kwargs
    utils.show_kwargs(**kwargs)

    # parse
    src_dir:Path = Path(kwargs["img_dir"])
    laplacian_threshold:int = kwargs['lt']
    descripter_threshold:int = kwargs['st']

    # search img paths
    img_paths:List[Path] = path_functions.search_img_paths(src_dir, [".jpg", ".png"])
    img_paths.sort()

    # make out dir
    out_dir:Path = src_dir.parent.joinpath(f"{src_dir}_non_dupricated")
    out_dir.mkdir(exist_ok=True)

    # ask user continue program
    is_skip_ask:bool = kwargs["y"]
    if not is_skip_ask:
        ask_start(**locals())

    # Extract non dupricate img
    ext_img_paths:List[Path]
    ext_laplacians:List[float]
    ext_img_paths, ext_laplacians = extract_by_laplacian(img_paths, laplacian_threshold)
    print(f"num_extracted {len(ext_img_paths):4} by extract_by_laplacian")


    # copy_img
    if kwargs["debug"]:
        for img_path, lap in zip(ext_img_paths, ext_laplacians):
            img:np.ndarray = cv2.imread(str(img_path))
            report_image(img, lap, "lap")
            out_file: Path = out_dir.joinpath(f"{img_path.stem}_lap.jpg")
            cv2.imwrite(str(out_file), img)


    sorted_idxes:List[int] = [ pair[0] for pair in sorted(enumerate(ext_laplacians), key=lambda x:x[1], reverse=True) ]
    ext_img_paths = [ ext_img_paths[idx] for idx in sorted_idxes ]
    ext_img_paths = extract_by_similarity(ext_img_paths, descripter_threshold)
    print(f"num_extracted {len(ext_img_paths):4} by extract_by_similarity")

    # copy_img
    for img_path in ext_img_paths:
        out_file: Path = out_dir.joinpath(img_path.name)
        shutil.copy(img_path, out_file)


def ask_start(*args, **kwargs):
    num_imgs:int = len(kwargs['img_paths'])
    print(f" start process with {num_imgs}? (y/n) >> ", end="")
    input_:str = input()
    if input_ not in ["y", "Y", "Yes", "yes"]:
        sys.exit(0)


def extract_by_laplacian(img_paths, thresh):
    dsc_img_paths: List[Path] = []
    dsc_laplacians: List[float] = []
    for img_path in tqdm.tqdm(img_paths, desc="by lapracian"):
        img = cv2.imread(str(img_path))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = variance_of_laplacian(gray_img)
        # report_image(img, laplacian, "Lap")
        if laplacian.var() > thresh:
            dsc_img_paths.append(img_path)
            dsc_laplacians.append(laplacian.var())
    return dsc_img_paths, dsc_laplacians


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F)


def report_image(image, laplacian_var, text):
    cv2.putText(image, "{}: {:.2f}".format(text, laplacian_var), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)


def extract_by_similarity(img_paths, thresh):
    sift = cv2.SIFT_create()

    # compute dess
    dess = []
    for img_path in tqdm.tqdm(img_paths, desc="compute descripter"):
        src_img = cv2.imread(str(img_path))
        gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        kpt, des = sift.detectAndCompute(gray_img, None)
        dess.append(des)

    # extract non similaly
    dsc_img_paths:List[Path] = extract_non_duplication(img_paths, dess, thresh)

    return dsc_img_paths


def extract_non_duplication(img_paths:List[Path], dess:list, thresh:int=3000):
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    src_img_paths = copy.copy(img_paths)
    src_dess = copy.copy(dess)
    dsc_img_paths = []

    start_time = time.time()
    while(len(src_img_paths) > 1):
        elapd_time = time.time() - start_time
        print(f"\rsimilarity compute, elapd:{elapd_time:10.3f}, 残り枚数:{len(src_img_paths):4}", end="")
        dsc_img_paths.append(src_img_paths.pop(0))
        curr_des = src_dess.pop(0)
        num_matches = []
        for des in src_dess:
            num_matches.append(len(bf.match(curr_des, des)))
        for idx in range(len(num_matches))[::-1]:
            if num_matches[idx] > thresh:
                src_img_paths.pop(idx)
                src_dess.pop(idx)
    print("")
    return dsc_img_paths


if __name__ == "__main__":
    cli_args:Dict[str, Any] = argparse()
    main(**cli_args)
