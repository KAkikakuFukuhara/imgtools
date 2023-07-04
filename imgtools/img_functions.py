from typing import Any, List, Dict, Optional, Tuple
from pathlib import Path
from argparse import ArgumentParser
import logging
import sys
import shutil

import tqdm
import numpy as np
import cv2

from . import path_functions
from . import utils

sift:Optional[Any] = None # cv2.SIFT
bf:Optional[Any] = None # cv2.BFMatcher


def load_img(path:Path) -> Optional[np.ndarray]:
    """ 画像を読み込む
        失敗時はNoneを返す。
    """
    try:
        img:np.ndarray = cv2.imread(str(path))
    except Exception as e:
        logging.warning(f"skip read img from {path}, because can't read img" )
        return None
    return img


def compute_num_matches(img_path1:Path, img_path2:Path) -> int:
    """ 2画像の類似特徴点の数を計算する。
        アルゴリズムはSIFTを用いる
    """
    img_paths:List[Path] = [img_path1, img_path2]
    kpts:List[Any] = []
    dess:List[Any] = []

    if globals()["sift"] is None:
        global sift
        global bf
        sift = cv2.SIFT_create()
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    assert sift is not None
    assert bf is not None

    for img_path in img_paths:
        src_img:Optional[np.ndarray] = load_img(img_path)
        if src_img is None:
            return -1

        gray_img:np.ndarray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        res:Tuple[Any, Any] = sift.detectAndCompute(gray_img, None)
        kpts.append(res[0])
        dess.append(res[1])

    matches:Any = bf.match(dess[0], dess[1])

    return len(matches)
