""" 画像群から前のフレームの似た画像を削除する。
"""
from typing import Any, List, Dict, Optional, Tuple
from pathlib import Path
from argparse import ArgumentParser
import logging
import sys
import shutil

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
    parser.add_argument("thresh", type=int, help="img matching threshold")
    parser.add_argument("--all_img", action="store_true")
    parser.add_argument("--y", action="store_true", help="skip ask process")


    return vars(parser.parse_args())


def main(*args, **kwargs):
    # show kwargs
    utils.show_kwargs(**kwargs)

    # parse
    src_dir:Path = parse_src_dir(kwargs["img_dir"], **locals())
    thresh:int = kwargs['thresh']
    all_mode = kwargs["all_img"]

    # search img paths
    img_paths:List[Path] = path_functions.search_img_paths(src_dir, [".jpg", ".png"])
    img_paths.sort()

    # ask user continue program
    is_skip_ask:bool = kwargs["y"]
    if not is_skip_ask:
        ask_start(**locals())

    # Extract non dupricate img
    if not all_mode:
        ext_img_paths:List[Path] = extract_non_duprication(img_paths, thresh)
    else:
        ext_img_paths:List[Path] = extract_non_duprication_all(img_paths, thresh)

    # out_dir
    out_dir:Path = src_dir.parent.joinpath(f"{src_dir}_non_dupricated")
    out_dir.mkdir(exist_ok=True)
    for img_path in ext_img_paths:
        shutil.copy(img_path, out_dir)


def parse_src_dir(path:str, **kwargs) -> Path:
    path_:Path = Path(path)
    utils.check_is_valid_dir(path_)
    return path_


def parse_out_dir(path:str, **kwargs) -> Path:
    is_use_default_dir:bool = path == "None"
    if is_use_default_dir:
        path_:Path = Path(f"{kwargs['src_dir']}_non_dupricated")
    else:
        path_ = Path(path)
    utils.check_is_valid_dir(path_.parent)
    return path_


def ask_start(*args, **kwargs):
    num_imgs:int = len(kwargs['img_paths'])
    print(f" start process with {num_imgs}? (y/n) >> ", end="")
    input_:str = input()
    if input_ not in ["y", "Y", "Yes", "yes"]:
        sys.exit(0)


def extract_non_duprication(img_paths:List[Path], thre:int) -> List[Path]:
    pre_img_path:Path = img_paths[0]
    dsc_img_paths:List[Path] = [pre_img_path]

    for img_path in tqdm.tqdm(img_paths[1:]):
        num_match:int = img_functions.compute_num_matches(pre_img_path, img_path)
        if num_match < thre:
            dsc_img_paths.append(img_path)
            pre_img_path = img_path

    return dsc_img_paths


def extract_non_duprication_all(img_paths:List[Path], thre:int) -> List[Path]:
    import copy
    temp_img_paths:List[Path] = copy.copy(img_paths)
    extracted:List[Path] = []

    while(len(temp_img_paths) > 0):
        dupricated_img_paths:List[Path] = []
        curr:Path = temp_img_paths.pop(0)
        print(f"残り候補枚数 {len(temp_img_paths):>4}")
        extracted.append(curr)
        for cand in tqdm.tqdm(temp_img_paths, desc="特徴点マッチングの経過"):
            num_match:int = img_functions.compute_num_matches(curr, cand)
            if num_match > thre:
                dupricated_img_paths.append(cand)
        for path in dupricated_img_paths:
            temp_img_paths.remove(path)

    return extracted


def compute_match_kpts(img_paths:List[Path]):
    pre_kpt = None
    pre_des = None

    sift = cv2.xfeatures2d.SIFT_create()
    num_kpt_list = []
    for img_path in tqdm.tqdm(img_paths):
        src_img:Optional[np.ndarray] = load_img(img_path) # BGR
        if src_img is None:
            continue

        gray_img:np.ndarray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        curr_kpt, curr_des = sift.detectAndCompute(gray_img, None)
        if pre_kpt is None:
            pre_kpt = curr_kpt
            pre_des = curr_des
            continue

        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(pre_des, curr_des)

        num_kpt = len(matches)
        num_kpt_list.append(num_kpt)

        pre_kpt = curr_kpt
        pre_des = curr_des

    txt = "\n".join(map(lambda x:str(x), num_kpt_list))
    with open("./result.txt", "w") as f:
        f.write(txt)


if __name__ == "__main__":
    cli_args:Dict[str, Any] = argparse()
    main(**cli_args)
