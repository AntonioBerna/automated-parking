import qrcode


class QRCodeMaker:
    def __init__(self, text):
        self.text = " ".join(text)
    
    def make(self):
        return qrcode.make(self.text).get_image()