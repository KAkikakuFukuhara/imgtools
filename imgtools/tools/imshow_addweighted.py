""" ２つの画像群ディレクトリから同様の名称の画像を合成した画像を表示するツール
"""
from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
from typing import Optional, Dict, Tuple

import numpy as np
import cv2

import _add_path

PathPair = Tuple[Optional[Path], Optional[Path]]

is_convert_alpha: bool = False
DEFAULT_IMG_SHAPE = (720, 1280, 3)


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("--debug", action="store_true", help="debug mode")
    parser.add_argument("--img_dir1", type=str, default='NONE', help="img dir1")
    parser.add_argument("--img_dir2", type=str, default="NONE", help="img_dir2")
    parser.add_argument("-e", "--embedding", action="store_true",
        help="Embedding Flag. "
        + "Embedding mean that if img dir2 background is black, use img dir1 img use backgounrd")
    return parser


def main(*args, **kwargs):
    myargs = MyArgs(**kwargs)

    if myargs.is_debug:
        id2path_pair: dict[int, PathPair] = {0:(None, None)}
    else:
        id2path_pair: dict[int, PathPair] = make_id2path_pair(myargs.img_dir1, myargs.img_dir2)

    imshow(id2path_pair, myargs.is_embedding)


class MyArgs:
    def __init__(self, *args, **kwargs):
        self.is_debug: bool = self._parse_is_debug(**kwargs)
        self.img_dir1: Path = self._parse_img_dir1(**kwargs)
        self.img_dir2: Path = self._parse_img_dir2(**kwargs)
        self.is_embedding: bool = self._parse_is_embedding(**kwargs)


    def _parse_is_debug(self, *args, **kwargs) -> bool:
        print(kwargs)
        return bool(kwargs['debug'])


    def _parse_img_dir1(self, *args, **kwargs) -> Path:
        path = Path(kwargs['img_dir1'])
        if not self.is_debug:
            assert path.exists()
            assert path.is_dir()
        return path


    def _parse_img_dir2(self, *args, **kwargs) -> Path:
        path = Path(kwargs['img_dir2'])
        if not self.is_debug:
            assert path.exists()
            assert path.is_dir()
        return path


    def _parse_is_embedding(self, **kwargs):
        return kwargs['embedding']


def imshow(id2path_pair: dict[int, PathPair], is_embedding:bool):
    global is_convert_alpha

    cv2.namedWindow("image")
    cv2.createTrackbar("bar1", "image", 0, 100, on_is_convert_alpha)
    cur_id = 0
    pre_id = -1
    max_id = len(list(id2path_pair.keys())) - 1
    x_img: np.ndarray; y_img: np.ndarray; z_img: np.ndarray
    try:
        while(True):
            if cur_id != pre_id:
                x_img, y_img = load_img_pair(cur_id, id2path_pair, is_embedding)
                is_convert_alpha = True
                pre_id = cur_id

            if not is_convert_alpha:
                z_img = z_img
            else:
                alpha = cv2.getTrackbarPos("bar1", "image") * 0.01
                beta = 1 - alpha
                z_img = cv2.addWeighted(x_img, beta, y_img, alpha, 0)
                is_convert_alpha = False

            cv2.imshow("image", z_img)
            key = cv2.waitKey(1) & 0xff

            if key == ord('q'):
                break
            if key == ord('f'):
                if cur_id < max_id:
                    cur_id += 1
            if key == ord('d'):
                if cur_id > 0:
                    cur_id -= 1
    finally:
        cv2.destroyAllWindows()


def on_is_convert_alpha(*args, **kwargs):
    global is_convert_alpha
    is_convert_alpha = True


def load_img_pair(id_: int, id2path_pair: dict[int, PathPair], is_embedding: bool) -> tuple[np.ndarray, np.ndarray]:
    x_path: Optional[Path]
    y_path: Optional[Path]
    x_path, y_path = id2path_pair[id_]
    if isinstance(x_path, Path):
        x = cv2.imread(str(x_path))
    else:
        x = np.zeros((DEFAULT_IMG_SHAPE), np.uint8)

    if isinstance(y_path, Path):
        y = cv2.imread(str(y_path))
    else:
        y = np.ones((DEFAULT_IMG_SHAPE), np.uint8) * 255

    x_w:int;x_h:int
    x_w, x_h = x.shape[:2][::-1]
    y = cv2.resize(y, (x_w, x_h))

    if is_embedding:
        y[y==[0, 0, 0]] = np.asanyarray(x[y==[0, 0, 0]] * 0.7, dtype=np.uint8)

    return x, y


def make_id2path_pair(dir1: Path, dir2: Path):
    img_suffixes = [".jpg", ".png"]
    img_paths1: list[Path] = search_img_paths(dir1, img_suffixes)
    img_paths2: list[Path] = search_img_paths(dir2, img_suffixes)

    assert len(img_paths1) > 0, f"Zero img in {dir1}"
    assert len(img_paths2) > 0, f"Zero img in {dir2}"

    stem2path_pair: dict[str, PathPair] = matching_by_stem(img_paths1, img_paths2)

    stems: list[str] = sorted(stem2path_pair.keys(), key=lambda x:x)
    id2path_pair: dict[int, PathPair] = {si:stem2path_pair[stem] for si, stem in enumerate(stems)}
    return id2path_pair


def search_img_paths(dir: Path, suffixes: list[str]):
    dir_:Path = Path(dir)
    assert dir_.exists()
    assert dir_.is_dir()

    assert len(suffixes) > 0, "Non elements in suffixes"
    for suf in suffixes:
        assert isinstance(suf, str), "Suffixes include non str"

    suffixes_:list[str] = suffixes + [suf.upper() for suf in suffixes] # [".jpg"] to [".jpg", ".JPG"]
    img_paths:list[Path] = [path for suf in suffixes_ for path in dir_.glob(f"*{suf}")]
    img_paths.sort()

    return img_paths


def matching_by_stem(paths1: list[Path], paths2: list[Path])  \
        -> dict[str, PathPair]:
    stem2path1: dict[str, Path] = {p.stem:p for p in paths1}
    stem2path2: dict[str, Path] = {p.stem:p for p in paths2}

    stems_set1 = set(list(stem2path1.keys()))
    stems_set2 = set(list(stem2path2.keys()))
    intersection = stems_set1 and stems_set2
    union = stems_set1 or stems_set2
    iou = len(intersection) / len(union)
    assert iou > 0.75, "２つのディレクトリの同名ファイルの数が十分でないためエラーとする"

    all_stems = list(union)
    all_stems.sort()

    stem2path_pair: dict[str, PathPair] = {}
    for stem in all_stems:
        path1: Optional[Path] = stem2path1.get(stem, None)
        path2: Optional[Path] = stem2path2.get(stem, None)
        stem2path_pair[stem] = (path1, path2)

    return stem2path_pair


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))
