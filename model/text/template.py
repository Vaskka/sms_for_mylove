# -*- coding: utf-8 -*-
import json
import random

import settings
from tool.util import *
from model.text.reply import Reply


class TextTemplate:

    # 原生配置文件dict
    inner_dict = dict()

    # 自动回复检查对象
    reply = None

    @classmethod
    def init_text_template(cls):
        """
        初始化信息模版
        :return: None
        """

        with open(settings.TEXT_TEMPLATE_SETTING_PATH, "r") as f:
            json_dict_text = f.read()

        # 加载文字模版dict
        cls.inner_dict = json.loads(json_dict_text)

        # 自动回复检查模块
        cls.reply = Reply(cls.inner_dict["auto_reply"])
        pass

    @classmethod
    def from_main_weather_get_comment(cls, main_weather):
        """
        从main_weather得到响应的评价
        :param main_weather: 主天气
        :return: str comment
        """

        for k, v in cls.inner_dict["comment"]["weather"].items():
            if k in main_weather:
                rand_index = random.randint(0, len(v) - 1)
                return v[rand_index]

        # 默认comment
        return "今天天气看起来不错呢"
        pass

    @classmethod
    def from_temperature_get_comment(cls, max_temperature, min_temperature):
        """
        从温度得到天气评论
        :param max_temperature: 最高气温
        :param min_temperature: 最低气温
        :return: str comment
        """

        max_t = int(select_with_regex("(.*?[0-9]*)°C", max_temperature))
        min_t = int(select_with_regex("(.*?[0-9]*)°C", min_temperature))

        # 检索天气
        if settings.TERM == 0 or settings.TERM == 3:
            if max_t > 32:
                t_list = cls.inner_dict["comment"]["temperature"]["hot"]
                pass
            elif min_t < 15:
                t_list = cls.inner_dict["comment"]["temperature"]["cold"]
                pass
            else:
                t_list = cls.inner_dict["comment"]["temperature"]["normal"]
        elif settings.TERM == 1 or settings.TERM == 2:
            if min_t < -20:
                t_list = cls.inner_dict["comment"]["temperature"]["cold"]
            else:
                t_list = cls.inner_dict["comment"]["temperature"]["normal"]
        else:
            t_list = cls.inner_dict["comment"]["temperature"]["normal"]

        # comment中随机取
        rand_index = random.randint(0, len(t_list) - 1)

        return t_list[rand_index]
        pass

    @classmethod
    def from_air_get_comment(cls, air_number):
        """
        从空气数据得到comment
        :param air_number: 空气指数
        :return: str comment
        """

        a_num = int(air_number)

        if 0 <= a_num <= 50:
            a_list = cls.inner_dict["comment"]["air"]["0"]
        elif 50 < a_num <= 100:
            a_list = cls.inner_dict["comment"]["air"]["1"]
        elif 100 < a_num <= 300:
            a_list = cls.inner_dict["comment"]["air"]["2"]
        elif a_num > 300:
            a_list = cls.inner_dict["comment"]["air"]["3"]
        else:
            a_list = cls.inner_dict["comment"]["air"]["1"]

        # comment中随机取
        rand_index = random.randint(0, len(a_list) - 1)

        return a_list[rand_index]
        pass

    @classmethod
    def get_lesson_text_template(cls, lesson_status):
        """
        根据课程状态得到文字模版
        :param lesson_status: 是否有课
        :return: 模版str
        """

        if lesson_status:
            random_index = random.randint(1, len(cls.inner_dict["template"]["lesson"]) - 1)
            return cls.inner_dict["template"]["lesson"][random_index]
            pass
        else:
            return cls.inner_dict["template"]["lesson"][0]

        pass

    @classmethod
    def get_news_text_template(cls):
        """
        得到新闻模版
        :return: 模版str
        """
        random_index = random.randint(0, len(cls.inner_dict["template"]["news"]) - 1)
        return cls.inner_dict["template"]["news"][random_index]

        pass

    @classmethod
    def check_switch_on_message(cls, message):
        """
        开启小萨时的功能检测
        :param message 发送来的message
        :return:
        """
        pass

    @classmethod
    def check_to_switch_on_message(cls, message):
        """
        关闭小萨时的功能检测(检查是否开启小萨)
        :param message 发送来的message
        :return: ReplyResult
        """
        pass
        return cls.reply.check_switch_on(message.text)
    pass

    @classmethod
    def check_face_image(cls, msg):
        """
        检查是否有前置功能待处理
        :return: ImageReplyResult
        """
        return cls.reply.check_front_function(msg=msg)
        pass

    @classmethod
    def check_main_function(cls, msg):
        """
        检查主要功能
        :param msg: message 对象
        :return: ReplyResult
        """
        return cls.reply.check_main_function(msg.text)
        pass

    @classmethod
    def close_front_function(cls):
        """
        关闭前置功能
        :return:
        """
        cls.reply.close_front()
        pass

    @classmethod
    def get_greeting_str(cls):
        """
        得到问候信息
        :return: str
        """
        main_li = cls.inner_dict["template"]["greeting"]

        rand_index = random.randint(0, len(main_li) - 1)
        return main_li[rand_index]
        pass

