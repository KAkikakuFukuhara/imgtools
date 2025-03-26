""" cv2を利用した画像の解像度のみの取得
"""
from typing import List
from argparse import ArgumentParser
from pathlib import Path
import time

import cv2


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("img_dir", type=str, help="img_dir")
    kwargs = vars(parser.parse_args())

    img_dir_path = Path(kwargs['img_dir'])
    assert img_dir_path.exists()

    img_paths: List[Path] = []
    suffixes = [".jpg", ".png"]
    for sfx in suffixes:
        for img_path in img_dir_path.glob(f"*{sfx}"):
            img_paths.append(img_path)
    img_paths.sort()


    elapd_time_list = []
    num_img_paths = len(img_paths)
    print("")
    for di in range(num_img_paths):
        start_time = time.time()
        img = cv2.imread(str(img_paths[di]))
        hsize: int; wsize: int; csize: int
        hsize, wsize, csize = img.shape
        elapd_time = time.time() - start_time

        elapd_time_list.append(elapd_time)

        print(f"\r{di+1:>5}/{num_img_paths}", end="")
    print("")

    print(f"SumTime : {sum(elapd_time_list):.3f} sec")
    print(f"MeanTime: {sum(elapd_time_list)/num_img_paths:.6f} sec")    

    # result
    # 5667/5667
    # SumTime : 85.704 sec
    # MeanTime: 0.015123 sec
