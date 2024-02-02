"""ディレクトリに含まれる画像の解像度を調べるプログラム
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Any, Dict, List
from pathlib import Path
import pprint

import tqdm
import numpy as np
import cv2

import _add_path
from imgtools import path_functions
from imgtools import utils


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("img_dir", type=str, help="target dir include imgs")
    return parser


def main(*args, **kwargs):
    utils.show_kwargs(**kwargs)

    img_dir:Path = Path(kwargs['img_dir'])
    utils.check_is_valid_dir(img_dir)
    print(f"Target dir is {img_dir}")

    img_paths:List[Path] = path_functions.search_img_paths(img_dir, [".jpg", ".png"])
    print(f"number of imgs is {len(img_paths)}")

    resolution2count:Dict[str, int] = count_process(img_paths)
    print("{WidthxHeight:num}")
    pprint.pprint(resolution2count)


def count_process(img_paths:List[Path]) -> Dict[str, int]:
    resolution2count:Dict[str, int] = {}
    for img_path in tqdm.tqdm(img_paths, desc="count resolution"):
        img:np.ndarray = cv2.imread(str(img_path)) #type:ignore

        hsize:int = img.shape[0]
        wsize:int = img.shape[1]
        resolution:str = f"{wsize}x{hsize}"
        if resolution not in resolution2count.keys():
            resolution2count[resolution] = 1
        else:
            resolution2count[resolution] += 1
    return resolution2count


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = add_arguments(parser)
    main(**vars(parser.parse_args()))