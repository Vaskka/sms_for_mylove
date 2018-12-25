# -*- coding: utf-8 -*-
import json
import os
import traceback

from wxpy import *

import settings
from model.base import BaseModel
from model.text.template import TextTemplate
from timer.maker import Timer


class LittleSa:
    bot = Bot(console_qr=(not settings.DEBUG))

    # 信息发送人
    if settings.DEBUG:
        mylove = bot.file_helper
    else:
        mylove = ensure_one(bot.friends().search(name=settings.MYLOVE_SENDER))

    auto_switch = False

    timer = Timer(settings.TASK_SETTING_PATH)

    template = TextTemplate()

    logger = get_wechat_logger(receiver=bot)

    tuling = None

    @classmethod
    def init_sa(cls):
        """
        初始化小萨
        :return: None
        """

        # 检查环境 初始化log文件
        cls._check_env()

        # 正在读取配置
        cls._read_setting()

        # 注册模型
        print("正在注册模型....")
        BaseModel.little_sa = cls

        # 初始化定时任务
        print("正在初始化定时任务....")
        cls.timer.do_register()

        # 初始化自动回复
        print("正在初始化自动回复与文字模型....")
        cls.template.init_text_template()

        print("正在唤醒小萨...")
        cls.tuling = Tuling(api_key=settings.TULING_API_KEY)

        # 注册自动回复
        print("正在注册自动回复....")
        cls._init_auto_reply()

        pass

    @staticmethod
    def _check_env():
        """
        检查环境创建日志
        :return:
        """
        # 日志目录创建
        point_main_dir = settings.POINT_MAIN_PATH

        if not os.path.exists(point_main_dir):
            os.mkdir(point_main_dir)
            pass

        # 检查各个模型文件夹
        for model in settings.ENABLE_FUNCTION:
            if not os.path.exists(os.path.join(point_main_dir, model)):
                os.mkdir(os.path.join(point_main_dir, model))

        pass

    @classmethod
    def _init_auto_reply(cls):
        """
        初始化自动回复
        :return:
        """

        @cls.bot.register(cls.mylove, TEXT)
        def auto_reply(msg):
            """
            自动回复
            :param msg: come message
            :return: str return message
            """
            try:
                if cls.auto_switch:
                    # 检查关闭
                    r_s = cls.template.get_to_switch_off(msg)
                    if r_s.reply_key:
                        cls.auto_switch = False
                        return r_s.reply_name

                    # 打开自动回复, 检查功能
                    result = cls.template.check_main_function(msg)

                    if result.reply_key:
                        return result.reply_name

                    # 不是功能调用bot
                    cls.tuling.do_reply(msg)
                    pass
                else:
                    # 关闭了自动回复
                    check_open = cls.template.check_to_switch_on_message(msg)
                    if check_open.reply_key:
                        # 开启小萨
                        cls.auto_switch = True
                        # 回复已经开启的消息
                        return check_open.reply_name
                    pass
            except:
                cls.logger.exception(traceback.format_exc())
                pass

        pass

        @cls.bot.register(cls.mylove, PICTURE)
        def auto_reply_pic(msg):
            """
            图片的自动回复
            :param msg: come message
            :return: str return message
            """
            try:
                if cls.auto_switch:
                    # 打开的自动回复
                    re = cls.template.check_face_image(msg)

                    if re.reply_key is not None:
                        if re.reply_key and re.tp == "beautify":
                            cls.mylove.send_image(os.path.join(settings.POINT_MAIN_PATH, "face", "_beautify_output.jpg"))
                            cls.mylove.send("这个就是美颜后的图片呐!")
                        elif re.reply_key and re.tp == "attr":
                            cls.mylove.send_image(os.path.join(settings.POINT_MAIN_PATH, "face", "_attr.jpg"))
                            cls.mylove.send(re.reply_name)
                        elif not re.reply_key and re.tp == "beautify":
                            cls.mylove.send(re.reply_name)

                        # 不论是否有响应都关闭前置功能
                        cls.template.close_front_function()
            except:
                cls.logger.exception(traceback.format_exc())
                pass

    pass

    @staticmethod
    def _read_setting():
        """
        读取配置文件
        :return:
        """
        with open(os.path.join(settings.POINT_MAIN_PATH, "main.json"), "r") as f:
            json_str = f.read()

        json_dict = json.loads(json_str)

        settings.TULING_API_KEY = json_dict["tuling"]
        settings.FACE_API_KEY = json_dict["face_api_key"]
        settings.FACE_API_SECRET = json_dict["face_api_secret"]
        settings.SHOW_API_KEY = json_dict["show_api_key"]
        pass