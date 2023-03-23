"""
画像関連の編集等のプログラムのコマンドラインパーサー
"""
import os
from typing import Any, List
from argparse import ArgumentParser, _SubParsersAction
import subprocess
from pathlib import Path

CURR_DIR:Path = Path(os.path.curdir).absolute()
FILE_DIR:Path = Path(__file__).absolute().parent
ROOT_DIR:Path = FILE_DIR.parent
PYTHON_PATH:Path = ROOT_DIR.joinpath(".venv/bin/python")

def parse_args():
    parser:ArgumentParser = ArgumentParser(prog="imgtools", description=__doc__)
    subparsers:_SubParsersAction = parser.add_subparsers()

    add_makeMP4(subparsers)
    add_count_resolution(subparsers)

    args:Any = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(args, parser)
    else:
        parser.print_help()


def main(*args, **kwargs):
    parse_args()


def add_makeMP4(subparser:_SubParsersAction):

    description:str = \
    """画像セットから動画を作成する
    """
    parser:ArgumentParser = subparser.add_parser("makeMP4", description=description)

    parser.add_argument("img_dir", type=str, help="dir has imgs")
    parser.add_argument("--fps", type=float, default=30, help="frame per seconds. default is 30")
    parser.add_argument("--out_file", type=str, default="./out.mp4", 
                        help="output file (mp4). default is './out.mp4'")
    parser.add_argument("--num_img", type=int, default=-1, help="limit num that img will be used")

    def event(*args):
        _args:Any = args[0]
        commands:List[str] = []
        commands += [str(PYTHON_PATH)]
        commands += [str(FILE_DIR.joinpath("cvt_img2mp4.py"))]
        commands += [_args.img_dir]
        commands += ["--fps", str(_args.fps)]
        commands += ["--out_file", str(_args.out_file)]
        commands += ["--num_img", str(_args.num_img)]
        subprocess.run(commands)

    parser.set_defaults(handler=event)


def add_count_resolution(subparser:_SubParsersAction):

    description:str = \
    """
    ディレクトリに含まれる画像の解像度を調べるプログラム
    """
    parser:ArgumentParser = subparser.add_parser("count_resolution", description=description)
    parser.add_argument("img_dir", type=str, help="target dir include imgs")

    def event(*args):
        _args:Any = args[0]
        commands:List[str] = []
        commands += [str(PYTHON_PATH)]
        commands += [str(FILE_DIR.joinpath("count_img_size.py"))]
        commands += [_args.img_dir]
        subprocess.run(commands)

    parser.set_defaults(handler=event)


if __name__ == "__main__":
    main()