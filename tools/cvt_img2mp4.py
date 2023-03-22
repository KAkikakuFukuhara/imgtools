""" 画像セットから動画を作成する
"""
import sys
from typing import Tuple, List, Dict, Any
from pathlib import Path
from argparse import ArgumentParser
import logging

import cv2
import tqdm

import _add_path
from imgtools import path_functions

logging.basicConfig(
    level=logging.DEBUG
)


def parse_args() -> Dict[str, Any]:
    parser = ArgumentParser()

    parser.add_argument("img_dir", type=str, help="dir has imgs")
    parser.add_argument("--fps", type=float, default=30, help="frame per seconds. default is 30")
    parser.add_argument("--out_file", type=str, default="./out.mp4", 
                        help="output file (mp4). default is './out.mp4'")
    parser.add_argument("--num_img", type=int, default=-1, help="limit num that img will be used")

    kwargs = vars(parser.parse_args())

    return kwargs


def main(*args, **kwargs):
    check_path(kwargs['img_dir'])
    check_positive(kwargs['fps'])
    if kwargs['num_img'] >= 0:
        check_positive(kwargs['num_img'])

    img_paths:List[Path] = path_functions.search_img_paths(kwargs['img_dir'], [".jpg", ".png"])

    if kwargs['num_img'] > 0:
        img_paths = img_paths[:kwargs['num_img']]

    dsc_img_shape = retrieve_mode_img_shape(img_paths)

    video_writer:cv2.VideoWriter = create_video_writer(
        kwargs['out_file'], kwargs['fps'], dsc_img_shape)

    write_video(video_writer, img_paths, dsc_img_shape)


def check_path(path:str):
    _path = Path(path)
    if not _path.exists():
        raise FileNotFoundError(str(_path))


def check_positive(value:float):
    if value < 0:
        raise ValueError(f"value is not positive. but is {value} ")


def retrieve_mode_img_shape(img_paths:List[Path]) -> Tuple[int, int, int]:
    logging.debug("Retrive most most value of img shape")
    shape2count = {}
    for path in img_paths:
        img = cv2.imread(f"{path}")
        img_shape = img.shape
        if img_shape not in shape2count:
            shape2count[img_shape] = 1
        else:
            shape2count[img_shape] += 1

    _list = [ (shape, cnt ) for shape, cnt in shape2count.items() ]
    _list = sorted(_list, key=lambda x:x[1], reverse=True)

    # show 3 top
    logging.info("[Info] img shapes from img_paths")
    i = 0
    for shape, cnt in _list:
        if i > 3:
            break
        logging.info(f"\tshape:{shape}, count:{cnt}")
        i+= 1

    mode_shape = _list[0][0]
    return mode_shape


def create_video_writer(out_path:str, fps:float, dsc_img_shape:Tuple[int, int, int]) -> cv2.VideoWriter:
    _path = Path(out_path)
    if _path.is_dir():
        dsc_path = _path.joinpath("out.mp4")
    else:
        if not _path.parent.exists():
            raise FileNotFoundError(f"{_path.parent}")
        dsc_path = Path(f"{_path.parent}/{_path.stem}.mp4")

    hsize = dsc_img_shape[0]
    wsize = dsc_img_shape[1]
    shape = (wsize, hsize)

    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(f"{dsc_path}", fmt, fps, shape)

    return writer


def write_video(video_writer:cv2.VideoWriter, img_paths:List[Path], dsc_img_shape:Tuple[int, int, int]):
    for path in tqdm.tqdm(img_paths, desc="wirte_img_to_video"):
        img = cv2.imread(str(path)) # bgr

        if img.shape == dsc_img_shape:
            dsc_img = img
        else:
            dsc_img = cv2.resize(img, (dsc_img[1], dsc_img[0]))

        video_writer.write(dsc_img)
    video_writer.release()


if __name__ == "__main__":
    kwargs = parse_args()
    main(**kwargs)