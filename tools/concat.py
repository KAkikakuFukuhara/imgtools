''' 画像を合成する
'''
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
    axis_num = 0 if kwargs['vertical'] else 1
    imgpaths1 = imgp.search_img_paths(dir1, suffixes=["jpg", "png"])
    imgpaths2 = imgp.search_img_paths(dir2, suffixes=["jpg", "png"])
    imgpaths1.sort()
    imgpaths2.sort()

    outdir = Path(kwargs['out']).joinpath("concated")
    utils.check_is_valid_dir(outdir.absolute().parent)
    outdir.mkdir(exist_ok=True)
    print(f"save to {outdir.absolute()}")

    min_num_imgpaths = min([len(imgpaths1), len(imgpaths2)])
    print(f"Num Imgs, MIN:{min_num_imgpaths}, DIR1:{len(imgpaths1)}, DIR2:{len(imgpaths2)}")
    for idx in tqdm.tqdm(range(min_num_imgpaths), desc="concat and write"):
        img1 = cv2.imread(str(imgpaths1[idx]))
        img2 = cv2.imread(str(imgpaths2[idx]))
        shapes = np.array([list(img1.shape), list(img2.shape)])
        max_hsize = max(shapes[:, 0])
        max_wsize = max(shapes[:, 1])
        canvas_shape = (max_hsize, max_wsize, 3)
        canvas1 = np.zeros(canvas_shape, np.uint8)
        canvas2 = canvas1.copy()
        canvas1[:shapes[0, 0], :shapes[0, 1], :] = img1
        canvas2[:shapes[1, 0], :shapes[1, 1], :] = img2
        concated = np.concatenate([canvas1, canvas2], axis=axis_num)
        out_file = outdir.joinpath(f"{imgpaths1[idx].stem}.png")
        cv2.imwrite(str(out_file), concated)


if __name__ == "__main__":
    main(**parse_args())