import base64
from argparse import ArgumentParser
from pathlib import Path

import cv2
import numpy as np


def bytes2numpy(img_bytes: bytes):
    ### decode to numpy
    npattr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(npattr, cv2.IMREAD_UNCHANGED)
    print(img.shape)
    return img


def imshow(img: np.ndarray):
    ### view
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ### parser
    parser = ArgumentParser()
    parser.add_argument("img", type=str, help=".jpg")
    args = parser.parse_args()

    ### check valid
    img_path = Path(args.img)
    assert img_path.exists()
    assert img_path.suffix == ".jpg"

    ### load binary
    with img_path.open("rb") as f:
        img_bytes = f.read()
    # print(img) #str

    img1 = bytes2numpy(img_bytes)
    # imshow(img)

    ### convert numpy to str
    img_str = base64.b64encode(img_bytes).decode()

    ### convert str to numpy
    img_bytes2 = base64.b64decode(img_str.encode())
    img2 = bytes2numpy(img_bytes2)
    imshow(img2)


    ### check equal img
    is_equal = (img1 != img2).sum() == 0
    print("is_equal:", is_equal)
