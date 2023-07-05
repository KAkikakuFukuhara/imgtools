import sys
from pathlib import Path

import PIL
from PIL import Image, PngImagePlugin
import pprint

FILE_DIR = Path(__file__).absolute().parent
ROOT_DIR = FILE_DIR.parent
DATA_DIR = ROOT_DIR.joinpath("data")

def parse_IHDR(data):
    data_dict = {}
    idx = 0
    data_dict["wsize"] = int.from_bytes(data[idx:idx+4], "big")
    idx += 4
    data_dict["hsize"] = int.from_bytes(data[idx:idx+4], "big")
    idx += 4
    data_dict["bit"] = int.from_bytes(data[idx:idx+1], "big")
    idx += 1
    data_dict["color_type"] = int.from_bytes(data[idx:idx+1], "big")
    idx += 1
    data_dict["compression"] = int.from_bytes(data[idx:idx+1], "big")
    idx += 1
    data_dict["filter"] = int.from_bytes(data[idx:idx+1], "big")
    idx += 1
    data_dict["interrace"] = int.from_bytes(data[idx:idx+1], "big")
    idx += 1
    return data_dict


if __name__ == "__main__":
    sample_img_path = DATA_DIR.joinpath("samples/sample-boat-400x300.png")

    image = Image.open(sample_img_path)
    chunks = PngImagePlugin.getchunks(image)
    chunkname2data = {}
    for ch in chunks:
        name = ch[0].decode("utf-8")
        if name not in ["IDAT", "IEND"]:
            chunkname2data[name] = ch[1]
            print(name)
    ihdr = parse_IHDR(chunkname2data["IHDR"])

    pprint.pprint(ihdr)