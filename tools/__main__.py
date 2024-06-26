"""
画像関連の編集等のプログラムのコマンドラインパーサー
"""
import os
from typing import Any, List
from argparse import ArgumentParser, _SubParsersAction, RawTextHelpFormatter
import subprocess
from pathlib import Path

CURR_DIR:Path = Path(os.path.curdir).absolute()
FILE_DIR:Path = Path(__file__).absolute().parent
ROOT_DIR:Path = FILE_DIR.parent
PYTHON_PATH:Path = ROOT_DIR.joinpath(".venv/bin/python")

def add_arguments(parser:ArgumentParser) -> ArgumentParser:
    subparsers:_SubParsersAction = parser.add_subparsers()

    add_makeMP4(subparsers)
    add_count_resolution(subparsers)
    add_resize(subparsers)
    add_rotate(subparsers)
    add_concat(subparsers)
    add_png2jpg(subparsers)
    add_rgb2gray(subparsers)
    add_imshow(subparsers)

    return parser


def main(*args, **kwargs):
    if "handler" in kwargs:
        handler = kwargs.pop('handler')
        handler(**kwargs)
    else:
        parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
        parser: ArgumentParser = add_arguments(parser)
        parser.print_help()


def add_makeMP4(subparser:_SubParsersAction):
    import cvt_img2mp4
    parser: ArgumentParser = subparser.add_parser(
        "makeMP4", help=cvt_img2mp4.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = cvt_img2mp4.add_arguments(parser)
    parser.set_defaults(handler=cvt_img2mp4.main)


def add_count_resolution(subparser:_SubParsersAction):
    import count_img_size
    parser: ArgumentParser = subparser.add_parser(
        "count_resolution", help=count_img_size.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = count_img_size.add_arguments(parser)
    parser.set_defaults(handler=count_img_size.main)


def add_resize(subparser:_SubParsersAction):
    import resize
    parser: ArgumentParser = subparser.add_parser(
        "resize", help=resize.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = resize.add_arguments(parser)
    parser.set_defaults(handler=resize.main)


def add_rotate(subparser:_SubParsersAction):
    import rotate
    parser: ArgumentParser = subparser.add_parser(
        "rotate", help=rotate.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = rotate.add_arguments(parser)
    parser.set_defaults(handler=rotate.main)


def add_concat(subparser:_SubParsersAction):
    import concat
    parser: ArgumentParser = subparser.add_parser(
        "concat", help=concat.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser =concat.add_arguments(parser)
    parser.set_defaults(handler=concat.main)


def add_png2jpg(subparser:_SubParsersAction):
    import png2jpg
    parser: ArgumentParser = subparser.add_parser(
        "png2jpg", help=png2jpg.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = png2jpg.add_arguments(parser)
    parser.set_defaults(handler=png2jpg.main)


def add_rgb2gray(subparser:_SubParsersAction):
    import cvt_rgb2gray
    parser: ArgumentParser = subparser.add_parser(
        "rgb2gray", help=cvt_rgb2gray.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = cvt_rgb2gray.add_arguments(parser)
    parser.set_defaults(handler=cvt_rgb2gray.main)


def add_imshow(subparser:_SubParsersAction):
    import imshow_addweighted
    parser: ArgumentParser = subparser.add_parser(
        "imshow", help=imshow_addweighted.__doc__, formatter_class=RawTextHelpFormatter)
    parser: ArgumentParser = imshow_addweighted.add_arguments(parser)
    parser.set_defaults(handler=imshow_addweighted.main)


if __name__ == "__main__":
    parser:ArgumentParser = ArgumentParser(
        description=__doc__, 
        formatter_class=RawTextHelpFormatter)
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))