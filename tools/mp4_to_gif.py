''' 動画をgifファイルに変換する
'''
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path

from PIL import Image
import cv2
import numpy as np


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("src", type=str, help="mp4 file")
    parser.add_argument(
        "--out",
        type=str,
        help="Out Gif File. Defaut is src.stem.gif")
    parser.add_argument(
        "--scale",
        type=float,
        default=0.5,
        help="Resize Scale. Defaut is 0.5. Range is 0 < scale < 1.0")
    parser.add_argument(
        "--skip_frame",
        type=float,
        default=1,
        help="skip frame number! Defaut is 1")
    return parser


def main(*args, **kwargs):
    myargs = MyArgs(**kwargs)

    cvt_mp4_to_gif(
        myargs.src,
        myargs.out,
        myargs.scale,
        myargs.skip_frame)

    print(" *** finish *** ")


class MyArgs:
    def __init__(self, *args, **kwargs):
        self.src: Path = self._parse_src(**kwargs)
        self.out: Path = self._parse_out(**kwargs)
        self.scale: float = self._parse_scale(**kwargs)
        self.skip_frame: int = self._parse_skip_frame(**kwargs)


    def _parse_src(self, *args, **kwargs) -> Path:
        src = Path(kwargs['src'])
        assert src.exists()
        assert src.suffix == ".mp4"
        return src


    def _parse_out(self, *args, **kwargs) -> Path:
        out_raw: str = kwargs['out']
        if out_raw is not None:
            out: Path = Path(out_raw)
        else:
            out = self.src

        if not out.suffix == ".gif":
            out = out.with_suffix(".gif")

        assert out.parent.exists()
        return out


    def _parse_scale(self, *args, **kwargs) -> float:
        scale: float = kwargs['scale']
        assert 0 < scale < 1
        return scale


    def _parse_skip_frame(self, *args, **kwargs) -> int:
        skip_frame: int = kwargs['skip_frame']
        assert skip_frame > 0
        return skip_frame


def cvt_mp4_to_gif(src: Path, out: Path, scale: float, skip_frame: int):
    pil_images: list[Image.Image] = load_frames(src, scale, skip_frame)
    assert len(pil_images) > 0
    print("load images")

    first_image = pil_images[0]
    first_image.save(
        str(out),
        save_all=True,
        append_images=pil_images[1:],
        loop=0,
        duration=1)
    print("finish make gif")


def load_frames(src: Path, scale: float, skip_frame: int) -> list[Image.Image]:
    assert 0 < scale < 1
    assert skip_frame > 0

    cap_file = cv2.VideoCapture(str(src)) #type:ignore
    assert cap_file.isOpened()

    img_wsize =  cap_file.get(cv2.CAP_PROP_FRAME_WIDTH) # type:ignore
    img_hsize = cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT) #type:ignore
    new_wsize = int(round(img_wsize * scale, 0))
    new_hsize = int(round(img_hsize * scale, 0))

    pil_images: list[Image.Image] = []
    frame_num = 1
    # cv2.namedWindow("image1") #type:ignore
    try:
        while(True):
            ret, frame = cap_file.read()
            if not ret:
                break
            if frame_num % skip_frame > 0:
                continue

            # cv2.imshow("image1", frame) #type:ignore

            frame = cv2.resize(frame, (new_wsize, new_hsize)) #type:ignore
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #type:ignore
            pil_images.append(Image.fromarray(frame))

            # key = cv2.waitKey(1) & 0xff #type:ignore
            # if key == ord('q'):
            #     break
    finally:
        # cv2.destroyAllWindows() #type:ignore
        pass
    return pil_images


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))
