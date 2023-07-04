from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import cv2

def imshow(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def fft(img):
    return np.fft.fft2(img)


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
    b_fft = fft(img[:, :, 0])
    breakpoint()


if __name__ == "__main__":
    main(**parse_args())