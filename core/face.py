import base64
import os
import re

import requests

import settings
from tool import util
from settings import POINT_MAIN_PATH


class Face:
    beautify_open_url = "https://api-cn.faceplusplus.com/facepp/beta/beautify"
    attr_open_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

    @classmethod
    def beautify(cls, image_b64):
        """
        美图功能
        :param image_b64: 待美图的b64
        :return: dict
        """
        data = {
            "api_key": settings.FACE_API_KEY,
            "api_secret": settings.FACE_API_SECRET,
            "image_base64": image_b64,
            "whitening": 100,
            "smoothing": 100
        }

        # 请求api
        resp = requests.post(url=cls.beautify_open_url, data=data)

        # 判断结果
        if resp.status_code == 200 and "error_message" not in resp.json():
            path = os.path.join(POINT_MAIN_PATH, "face", "_beautify_output.jpg")
            with open(path, "wb") as f:
                f.write(base64.b64decode(resp.json()["result"]))

            return {
                "type": "SUCCESS",
                "result": path
            }
        else:
            error_dict = {
                "type": "FAILED",
                "result": "小萨这个功能好像坏掉了诶！\n!! > < !!，快叫主人修好我~"
            }

            # api文档上面的错误提示
            if resp.status_code == 400 and re.match("IMAGE_ERROR_UNSUPPORTED_FORMAT", resp.json()["error_message"]):
                error_dict["result"] = "这张图片好像坏掉了诶...换一张再试试吧~"
            elif resp.status_code == 400 and re.match("INVALID_IMAGE_SIZE", resp.json()["error_message"]):
                error_dict["result"] = "这张图片有点问题诶, 换一张再试试吧~"
            elif resp.status_code == 400 and re.match("IMAGE_FILE_TOO_LARGE", resp.json()["error_message"]):
                error_dict["result"] = "图片太大啦, 小萨看不完啦, 换一张再试试吧~"

            return error_dict
        pass

    @classmethod
    def attr(cls, image_b64):
        """
        人脸特征
        :param image_b64: b64
        :return: 完成评论的str
        """
        data = {
            "api_key": settings.FACE_API_KEY,
            "api_secret": settings.FACE_API_SECRET,
            "image_base64": image_b64,
            "return_attributes": "gender,age,smiling,emotion,beauty"
        }

        resp = requests.post(url=cls.attr_open_url, data=data)

        # 分析结论
        return cls._analysis_attr(resp.json())

    @classmethod
    def _analysis_attr(cls, json_dict):
        """
        分析图片信息特点得到结论
        :param json_dict: dict
        :return: str
        """
        result = ""

        count = 0
        for face in json_dict["faces"]:
            text_item = ""

            # 处理颜色
            color = settings.FACE_ATTR_RECT_COLOR[count]
            text_item += ("画着" + color["comment"] + "的是一位")

            # 处理性别
            gender = face["gender"]
            if gender["value"] == "Male":
                text_item += "小哥哥, 他"

                # 后面用到性别的填充模版及颜值
                gender_template = ("小哥哥", "他")
                beauty = face["beauty"]["male_score"]
            else:
                text_item += "小姐姐, 她"

                # 后面用到性别的填充模版及颜值
                gender_template = ("小姐姐", "她")
                beauty = face["beauty"]["female_score"]
                pass

            # 处理年龄
            age = face["age"]
            text_item += ("看起来有" + age["value"] + "岁了呀。")

            # 处理情绪
            # 拿到最明显的情绪
            max_em_value = face["emotion"].items()[0]
            for em in face["emotion"].items():
                if em[1] > max_em_value[1]:
                    max_em_value = em

            text_item += ("%s看起来很%s呢，" % (gender_template[0], settings.FACE_EMOTION[max_em_value[0]]))

            # 处理笑容
            if face["smile"]["value"] > face["smile"]["threshold"]:
                smile_tuple = ("有", "！")
            else:
                smile_tuple = ("没有", "。")

            text_item += ("%s好像%s在笑诶%s" % (gender_template[1], smile_tuple[0], smile_tuple[1]))

            # 处理颜值
            if beauty < 60:
                text_item += ("颜值评分:%f, emmmm..." % beauty)
            elif 60 <= beauty <= 70:
                text_item += ("颜值评分:%f, 这个%s勉强及格啦~" % (beauty, gender_template[0]))
            elif 70 < beauty <= 80:
                text_item += ("颜值评分:%f, 这个%s还挺好看的嘛!" % (beauty, gender_template[0]))
            else:

                if gender_template[1] == '他':
                    inner_comment = ("帅", "怎么会有这么帅的人嘛~")
                    text_item += ("颜值评分:%f！这个%s简直%s炸！%s" % (beauty, gender_template[0], inner_comment[0], inner_comment[1]))
                else:
                    inner_comment = ["简直美哭了呜呜呜...", "小萨想要这个小姐姐的联系方式！！啊啊啊！！！"]
                    if beauty < 90:
                        text_item += ("颜值评分:%f！%s" % (beauty, inner_comment[0]))
                    else:
                        text_item += ("颜值评分:%f！%s" % (beauty, inner_comment[1]))

            text_item += "\n"

            # 画线
            util.draw_rect_in_pic(os.path.join(settings.POINT_MAIN_PATH, "face", "_attr.jpg"), face["face_rectangle"], color["rgb"])
            count += 1
            result += text_item

            pass

        return result
        pass
