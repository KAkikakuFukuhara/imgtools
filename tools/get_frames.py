""" mp4 ファイルから画像データを抜き出して保存する
"""
from pathlib import Path
from argparse import ArgumentParser

import cv2
import tqdm


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("mp4", type=str, help="mp4 file")
    parser.add_argument("--dst_root", type=str, default="None", help="dst root dir. Default is mp4 file dir.")
    parser.add_argument("--debug", action="store_true", help="debug-mode")
    return parser


def main(*args, **kwargs):
    ### checking kwargs
    movie_path = Path(kwargs["mp4"])
    assert movie_path.exists()
    assert movie_path.suffix in ".mp4"

    if kwargs["dst_root"] == "None":
        dst_root_path = movie_path.parent
    else:
        dst_root_path = Path(kwargs["dst_root"])
    assert dst_root_path.is_dir()

    is_debug: bool = kwargs['debug']

    ### dst dir setting
    dst_dir_name = f"{movie_path.stem}_imgs"
    dst_dir_path: Path = dst_root_path.joinpath(dst_dir_name)

    ### Video Setting
    cap = cv2.VideoCapture(str(movie_path))
    num_frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ### show details
    txt = ""
    txt += "----- details ------\n"
    txt += "動画(mp4)から画像を抽出するプログラム\n"
    txt += "- 入力動画\n"
    txt += "\t- {}\n".format(movie_path)
    txt += "- 出力ディレクトリ\n"
    txt += "\t- {}\n".format(dst_dir_path)
    txt += "- 出力予定枚数\n"
    txt += "\t- {}\n".format(num_frames)
    txt += "\n\n"
    print(txt)

    ### main process
    print("ctrl+cで終了")
    for fi in tqdm.tqdm(range(num_frames)):
        try:
            ret, frame = cap.read()

            ### debug mode prcess
            if is_debug:
                ### show frame with window
                if "img_viewer" not in locals(): # create first time
                    img_viewer = DebugImgViewer()
                img_viewer.show(frame)
            else:
                ### imwrite
                if not dst_dir_path.exists():
                    dst_dir_path.mkdir()
                dst_file: Path = dst_dir_path.joinpath(f"{fi:06}.png")
                cv2.imwrite(str(dst_file), frame)

        except KeyboardInterrupt:
            break


class DebugImgViewer:
    def __init__(self):
        self._window_name = "img1"


    def __del__(self):
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            pass


    def show(self, img):
        cv2.imshow(self._window_name, img)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            raise Exception("press 'q' key")

        if cv2.getWindowProperty(self._window_name, cv2.WND_PROP_VISIBLE) < 1:
            raise Exception("Press 'x' in GUI")


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))
