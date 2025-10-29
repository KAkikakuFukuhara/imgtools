from argparse import ArgumentParser
import cv2


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("url", type=str, help="url")
    return parser


def main(*args, **kwargs):
    # 参考：https://www.codevace.com/py-opencv-qrcodeencoder/
    url = str(kwargs['url'])
    qr_params = cv2.QRCodeEncoder_Params()
    qr_params.mode = cv2.QRCODE_ENCODER_MODE_ECI
    qr_params.structure_number = 1

    qr_encoder = cv2.QRCodeEncoder.create(qr_params)
    qr_img = qr_encoder.encode(url)
    # cv2.imshow('img', qr_img)
    # cv2.waitKey(0)
    cv2.imwrite("qr_img.png", qr_img)


def set_qr_params_version(qr_params: cv2.QRCodeEncoder_Params ,text: str):
    num_text: int = get_url_length(text)
    level = 1
    version = compute_version(num_text, level)
    qr_params.version = version
    qr_params.correction_level = cv2.QRCODE_ENCODER_CORRECT_LEVEL_Q


def get_url_length(text: str):
    return len(text)


def compute_version(num_text: int, level: int):
    # 参考：https://www.qrcode.com/about/version.html
    # 今回は適当
    return 5


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))
