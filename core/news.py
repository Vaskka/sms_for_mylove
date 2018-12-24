# -*- coding: utf-8 -*-
import json
import os
import random

import requests

import settings
from lib.ShowapiRequest import ShowapiRequest


class News:

    @classmethod
    def send_news(cls, little_sa):
        """
        发送每日壁纸
        :param little_sa: 小萨引用
        :return: None
        """
        result_dict = cls._get_news_dict()

        little_sa.mylove.send("汪汪汪～这个是小萨给女主人找的好看的壁纸～🌱")
        little_sa.mylove.send_image(os.path.join(settings.POINT_MAIN_PATH, "news", "today.jpg"))

        text = result_dict["title"] + "\n" + result_dict["description"]
        little_sa.mylove.send(text)

        return json.dumps(result_dict)

        pass

    @classmethod
    def _get_news_dict(cls):
        """
        储存图片
        返回标题和内容文案
        :return:
        """
        settings.SHOW_API_KEY = "1650f6ae86a0486c99fdf2e6a331ff16"
        r = ShowapiRequest("http://route.showapi.com/1287-1", "83819", settings.SHOW_API_KEY)
        res = r.post()

        data = res.json()["showapi_res_body"]["data"]

        rand_index = random.randint(0, len(settings.USER_AGENT) - 1)
        ua = settings.USER_AGENT[rand_index]

        header = {
            "User-Agent": ua
        }

        result_img = requests.get(url=data["img_1366"], headers=header)

        with open(os.path.join(settings.POINT_MAIN_PATH, "news", "today.jpg"), "wb") as f:
            f.write(result_img.content)

        return {
            "title": data["title"],
            "description": data["description"],
            "url": data["img_1366"]
        }
        pass

    pass