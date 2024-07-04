"""画像のバイト列への変換
"""
from argparse import ArgumentParser
from pathlib import Path
import io
import base64
import time

from PIL import Image
import numpy as np
import cv2


def img_enc(img) -> bytes:
    is_ok: bool
    img_png: np.ndarray
    is_ok, img_png = cv2.imencode(".png", img)
    img_enc: bytes = img_png.tobytes()
    return img_enc


def img_dec(img_enc: bytes) -> np.ndarray:
    img_compressed:np.ndarray = np.frombuffer(img_enc, dtype=np.uint8)
    img:np.ndarray = cv2.imdecode(img_compressed, cv2.IMREAD_UNCHANGED)
    return img


def bytes2str(data: bytes) -> str:
    return data.decode()


def str2bytes(data: str) -> bytes:
    return data.encode()


def bytes2base64bytes(data: bytes) -> bytes:
    return base64.b64encode(data)


def base64bytes2bytes(data: bytes) -> bytes:
    return base64.b64decode(data)


def img_enc_and_dec1(img: np.ndarray):
    print(f"src img shape is {img.shape}")

    start_time = time.time()
    src_img_enc = img_enc(src_img)
    start_time = print_time(start_time)

    img_str = bytes2str(bytes2base64bytes(src_img_enc))
    start_time = print_time(start_time)

    dst_img_enc = base64bytes2bytes(str2bytes(img_str))
    start_time = print_time(start_time)

    dst_img = img_dec(dst_img_enc)
    start_time = print_time(start_time)

    # breakpoint()
    print(f"dst img shape is {dst_img.shape}")


def print_time(start_time: float):
    curr_time = time.time()
    elapd_time = curr_time - start_time
    print(f"elapd_time: {elapd_time}")
    return curr_time


def img_enc2(img:np.ndarray):
    hsize: int; wsize: int; csize: int
    hsize, wsize, csize = img.shape
    return img.shape, img.tobytes()


def img_dec2(img_enc: bytes, shape: tuple):
    img_compressed:np.ndarray = np.frombuffer(img_enc, dtype=np.uint8)
    img = np.reshape(img_compressed, shape)
    return img


def img_enc_and_dec2(img: np.ndarray):
    print(f"src img shape is {img.shape}")

    start_time = time.time()
    shape, src_img_enc = img_enc2(src_img)
    start_time = print_time(start_time)

    img_str = bytes2str(bytes2base64bytes(src_img_enc))
    start_time = print_time(start_time)

    dst_img_enc = base64bytes2bytes(str2bytes(img_str))
    start_time = print_time(start_time)

    dst_img = img_dec2(dst_img_enc, shape)
    start_time = print_time(start_time)

    # breakpoint()
    print(f"dst img shape is {dst_img.shape}")


if __name__ == "__main__":
    src_img = np.random.randint(0, 255, (480, 640, 3), np.uint8)
    # src_img = cv2.imread("")
    img_enc_and_dec1(src_img)
    img_enc_and_dec2(src_img)

