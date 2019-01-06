class FacePicFormatNotSupportException:
    """
    图片格式不支持
    """
    def __init__(self, msg, fmt):
        self.message = msg
        self.format = fmt