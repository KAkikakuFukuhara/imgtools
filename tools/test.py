from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import cv2

def imshow(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def value_of_laplacian(img):
    return cv2.Laplacian(img, cv2.CV_64F)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("img_dir")

    return vars(parser.parse_args())


def main(*args, **kwargs):
    img_dir = Path(kwargs["img_dir"])
    assert img_dir.exists()
    img_paths = list(img_dir.glob("*.jpg"))
    assert len(img_paths) > 0

    img = cv2.imread(str(img_paths[2]))
    lap_img = value_of_laplacian(img)
    imshow(lap_img)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lap2_img = value_of_laplacian(hsv_img[:, :, 2])
    imshow(lap2_img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap3_img = value_of_laplacian(gray_img)
    imshow(lap3_img)
    breakpoint()


if __name__ == "__main__":
    main(**parse_args())