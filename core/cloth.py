# -*- coding: utf-8 -*-
import json
import random

import requests

import settings


class WashCloth:

    @classmethod
    def check_wash_cloth(cls):
        """
        检查洗衣街得到响应的文字信息模版
        :return: str
        """
        data = {
            "machineId": "a6fe2487-e632-4312-ad09-05f9a6cb4195"
        }

        random_index = random.randint(0, len(settings.USER_AGENT) - 1)
        headers = {
            "User-Agent": settings.USER_AGENT[random_index]
        }

        detail_res = requests.post(url="https://userapi.qiekj.com/machine/detail", headers=headers, data=data)
        detail_dict = json.loads(detail_res.text)

        if detail_dict["data"]["remainTime"] == 0 or detail_dict["data"]["remainTime"] is None:
            return str("现在可以用哦，快去洗吧～")
        else:
            time_sec = detail_dict["data"]["remainTime"]
            minute = int(time_sec / 60)
            sec = time_sec % 60

        return str("现在有人哦，不过%d分%d秒后就可以去洗衣服啦～" % (minute, sec))
    pass
