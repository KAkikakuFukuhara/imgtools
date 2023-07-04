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

    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    for img_path in tqdm.tqdm(img_paths):
        img = cv2.imread(str(img_path))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = variance_of_laplacian(gray_img)
        report_image(img, laplacian, "Lap")
        out_file = out_dir.joinpath(img_path.name)
        cv2.imwrite(str(out_file), img)


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F)


def report_image(image, laplacian, text):
    cv2.putText(image, "{}: {:.2f}".format(text, laplacian.var()), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)


def copy_imgs(img_paths):
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    for img in img_paths:
        out_flie = out_dir.joinpath(img.name)
        shutil.copy(img, out_flie)

if __name__ == "__main__":
    main(**argparse())