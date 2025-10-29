""" https://www.codevace.com/py-opencv-qrcodeencoder/
"""
import cv2


# QRコードにする文字列
encoded_info = "漢字テスト"  
# QRコード エンコーダーの設定
qr_params = cv2.QRCodeEncoder_Params()
qr_params.correction_level = cv2.QRCODE_ENCODER_CORRECT_LEVEL_Q
qr_params.mode = cv2.QRCODE_ENCODER_MODE_AUTO
qr_params.version = 2 # 設定可能な値 1-40
qr_params.structure_number = 1

# QRCodeEncoderクラスのインスタンスを作成
QRencoder = cv2.QRCodeEncoder.create(qr_params)
# QRコードを作成
qrcode = QRencoder.encode(encoded_info)

cv2.imshow("img", qrcode)
cv2.waitKey(0)
