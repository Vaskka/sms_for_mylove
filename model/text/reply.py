import base64
import os

import settings
from core import face, cloth
from tool.util import select_with_regex, trans_img


class Reply:
    def __init__(self, reply_dict):
        self.reply_dict = reply_dict

        self.front_function_switch = {
            "switch": False,
            "classify": ""
        }
        pass

    def close_front(self):
        """
        关闭前置功能
        :return:
        """
        self.front_function_switch["switch"] = False
        self.front_function_switch["classify"] = ""
        pass

    def check_front_function(self, msg):
        """
        检查是否有前置功能
        :param msg message object
        :return:
        """
        if self.front_function_switch["switch"]:
            if self.front_function_switch["classify"] == "beautify":

                # 储存文件
                # 拿到文件格式
                fmt = select_with_regex(regex="^.*\.(.*)$", s=msg.file_name)
                temp_path = os.path.join(settings.POINT_MAIN_PATH, "face", "_beautify_input.%s" % fmt)
                correct_path = os.path.join(settings.POINT_MAIN_PATH, "face", "_beautify_input.jpg")
                msg.get_file(save_path=temp_path)

                # 转换为jpg
                trans_img(temp_path)

                # 处理美颜
                with open(correct_path, "rb") as f:
                    bs = f.read()

                re = face.Face.beautify(base64.b64encode(bs))

                # 内容是处理后图片的路径
                return FaceReplyResult(re["result"], re["type"] == "SUCCESS", "beautify")
            if self.front_function_switch["classify"] == "attr":
                # 储存文件
                # 拿到文件格式
                fmt = select_with_regex(regex="^.*\.(.*)$", s=msg.file_name)
                temp_path = os.path.join(settings.POINT_MAIN_PATH, "face", "_attr_input.%s" % fmt)
                correct_path = os.path.join(settings.POINT_MAIN_PATH, "face", "_attr_input.jpg")
                msg.get_file(save_path=temp_path)

                # 转换为jpg
                trans_img(temp_path)
                # 处理人脸分析
                with open(correct_path, "rb") as f:
                    bs = f.read()

                re = face.Face.attr(base64.b64encode(bs))

                # 内容是处理后的消息
                return FaceReplyResult(re, True, "attr")
        else:
            return FaceReplyResult(None, False, None)

        pass

    def check_main_function(self, message):
        """
        检查message对应的功能，调用对应的Model.run()
        :param message: str
        :return: None
        """

        if message == self.reply_dict["mylove"]["face"]["beautify"]:
            self.front_function_switch["switch"] = True
            self.front_function_switch["classify"] = "beautify"
            return ReplyResult("快把想要美颜的图片发给小萨叭，小萨很厉害的哟!", True)
        elif message == self.reply_dict["mylove"]["face"]["attr"]:
            self.front_function_switch["switch"] = True
            self.front_function_switch["classify"] = "attr"
            return ReplyResult("快把想要让小萨看的图片发给小萨叭，小萨很厉害的哟!", True)
        elif message == self.reply_dict["cloth"]["cloth"]:
            return ReplyResult(cloth.WashCloth.check_wash_cloth(), True)
        else:
            return ReplyResult(None, False)
        pass

    def check_switch_on(self, message):
        """
        检查是否开启
        :return: ReplyResult
        """

        if message == self.reply_dict["mylove"]["close"]["switch_on"]:
            return ReplyResult(self.reply_dict["little_sa"]["reply_mapping"]["switch_on"], True)
        else:
            return ReplyResult(None, False)
        pass
    pass


class ReplyResult:

    def __init__(self, content, status):

        # 自动回复的内容
        self.reply_name = content

        # 自动回复的状态
        self.reply_key = status
    pass


class FaceReplyResult:
    """
    人脸类型回复信息
    """

    def __init__(self, content, status, tp):
        super(FaceReplyResult, self).__init__(content, status)
        self.tp = tp
        pass
