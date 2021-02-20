import pyqrcode


class QRGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_qr(product_code):
        qrcode = pyqrcode.create(product_code)
        qr_file = 'images/qr_codes/' + f"{product_code}.png"
        qrcode.png(qr_file, scale=2, quiet_zone=2)
