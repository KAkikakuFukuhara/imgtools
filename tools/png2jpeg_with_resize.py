#!/home/fukuhara/anaconda3/envs/Opencv/bin/python
import sys
import os
import glob
import pathlib
from typing import List
import tqdm
from argparse import ArgumentParser

import numpy as np
import cv2

FILE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_TXT = "[{:<8}] {}"

def argparse():
    parser = ArgumentParser()

    parser.add_argument("png_img_dir", default=f"{FILE_DIR}/png_images")
    args = vars(parser.parse_args())

    return args

def get_png_paths(dir:str) -> List[str]:
    paths = []
    for extension in {'png', 'PNG'}:
        paths += glob.glob(f"{dir}/*.{extension}")

    return paths

def resize(src_img:np.ndarray, max_size=640):
    hsize, wsize, csize = src_img.shape

    if hsize > wsize:
        ratio = max_size / hsize
        resized_hsize = max_size
        resized_wsize = int(wsize * ratio)
    else:
        ratio = max_size / wsize
        resized_hsize = int(hsize * ratio)
        resized_wsize = max_size
    
    out_img = cv2.resize(src_img, (resized_wsize, resized_hsize))
    return out_img

if __name__ == "__main__":
    args = argparse()

    src_dir = pathlib.Path(args['png_img_dir'])
    out_dir = pathlib.Path(f"./jpg_images")

    assert src_dir.exists()
    if not out_dir.exists():
        out_dir.mkdir()
        print(LOG_TXT.format("INFO", f"make dir {out_dir}"))

    png_paths = get_png_paths(src_dir)
    if len(png_paths) == 0:
        print(LOG_TXT.format("ERROR", "target directory have no png"))
        sys.exit(0)

    for p in tqdm.tqdm(png_paths):
        try:
            path = pathlib.Path(p)
            src_img = cv2.imread(str(path))

            out_img = resize(src_img)
            out_path = f"{out_dir}/{path.stem}.jpg"
            cv2.imwrite(out_path, out_img)
        except Exception as e:
            print(e)
    print(LOG_TXT.format("DONE", "Exit Program"))
    
