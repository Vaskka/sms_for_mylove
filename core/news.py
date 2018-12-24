import base64
import json
import os
import random
import re

import requests
from lxml import etree

from model.text import template
from settings import POINT_MAIN_PATH


class News:
    base_url = "https://news.sina.com.cn/china/"
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0"
    }

    @classmethod
    def send_news(cls, little_sa):
        """
        发送新闻
        :param little_sa: 小萨引用
        :return: None
        """
        result_list = cls._get_news_dict()

        text = template.TextTemplate.get_news_text_template()
        little_sa.mylove.send(text)

        for di in result_list:
            little_sa.mylove.send_image(di["img"]["img_file_path"])

            r_i = random.randint(0, 100)

            if r_i % 2 == 0:
                little_sa.mylove.send(di["content"] + "\n" + "详情在这里, 汪~" + di["url"])
            else:
                little_sa.mylove.send(di["content"] + "\n" + "详情在这里, 喵~" + di["url"])

            pass

        return json.dumps(result_list)

        pass

    @classmethod
    def _get_news_dict(cls):
        res = requests.get(url=cls.base_url, headers=cls.header)

        parser = etree.HTML(str(res.content, "utf-8"))

        re_li = list()

        for i in range(1, 4):
            # 新闻标题 url
            content = str(parser.xpath("//div[@id='picBox']/ul[1]/li[%d]/a/span[1]/img/@alt" % i)[0])
            url = str(parser.xpath("//div[@id='picBox']/ul[1]/li[%d]/a/@href" % i)[0])

            # 图片url
            img_url = "http:" + str(parser.xpath("//div[@id='picBox']/ul[1]/li[%d]/a/span[1]/img/@src" % i)[0])

            # 判断图片格式
            format_result = re.match(".*\.(.*)", img_url)

            if format_result:
                img_format = format_result.group(1)
            else:
                img_format = ".jpg"

            # img文件名
            img_file = "news_pic_%d.%s" % (i, img_format)

            # 请求图片
            img_response = requests.get(url=img_url, headers=cls.header)
            img_file = os.path.join(POINT_MAIN_PATH, "news", img_file)
            with open(img_file, "wb") as f:
                f.write(img_response.content)
                pass

            r_dict = {
                "content": content,
                "url": url,
                "img": {
                    "img_url": img_url,
                    "img_file_path": img_file
                }
            }

            re_li.append(r_dict)

        return re_li
        pass

    pass