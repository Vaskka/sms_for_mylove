import json
import os

from wxpy import *

import settings
from model.base import BaseModel
from model.text.template import TextTemplate
from timer.maker import Timer


class LittleSa:
    def __init__(self):
        """
        小萨主体
        """
        # bot object
        self.bot = Bot(console_qr=(not settings.DEBUG))

        # 信息发送人
        if settings.DEBUG:
            self.mylove = self.bot.file_helper
        else:
            self.mylove = ensure_one(self.bot.friends().search(name=settings.MYLOVE_SENDER))

        # 自动回复的开关
        self.auto_switch = False

        # 定时器
        self.timer = Timer(settings.TASK_SETTING_PATH)

        # 文字模版与自动回复模块
        self.template = TextTemplate()
        self.tuling = None
        pass

    def init_sa(self):
        """
        初始化小萨
        :return: None
        """

        # 检查环境 初始化log文件
        self._check_env()

        # 正在读取配置
        self._read_setting()

        # 注册模型
        print("正在注册模型....")
        BaseModel.little_sa = self

        # 初始化定时任务
        print("正在初始化定时任务....")
        self.timer.do_register()

        # 初始化自动回复
        print("正在初始化自动回复与文字模型....")
        self.template.init_text_template()

        # 注册自动回复
        print("正在注册自动回复....")
        self._init_auto_reply()

        print("正在唤醒小萨...")
        self.tuling = Tuling(api_key=settings.TULING_API_KEY)
        pass

    def _check_env(self):
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

    def _init_auto_reply(self):
        """
        初始化自动回复
        :return:
        """
        @self.bot.register(self.mylove, TEXT)
        def auto_reply(msg):
            """
            自动回复
            :param msg: come message
            :return: str return message
            """
            if self.auto_switch:
                # 打开自动回复, 检查功能
                result = self.template.reply.check_main_function(msg)
                if result.reply_key:
                    return result.reply_name

                # 不是功能调用bot
                self.tuling.do_reply(msg)
                pass
            else:
                # 关闭了自动回复
                check_open = self.template.check_to_switch_on_message(msg)
                if check_open.reply_key:
                    # 开启小萨
                    self.auto_switch = True
                    # 回复已经开启的消息
                    self.mylove.send(check_open.reply_name)
                pass
            pass

        pass

        @self.bot.register(self.mylove, PICTURE)
        def auto_reply_pic(msg):
            """
            图片的自动回复
            :param msg: come message
            :return: str return message
            """
            if self.auto_switch:
                # 打开的自动回复
                re = self.template.check_face_image(msg)

                if re.type is not None:
                    if re.reply_key and re.type == "beautify":
                        self.mylove.send_image(os.path.join(settings.POINT_MAIN_PATH, "_beautify_output.jpg"))
                        self.mylove.send("这个就是美颜后的图片呐!")
                    elif re.reply_key and re.type == "attr":
                        self.mylove.send_image(os.path.join(settings.POINT_MAIN_PATH, "_attr.jpg"))
                        self.mylove.send(re.reply_name)
                    elif not re.reply_key and re.type == "beautify":
                        self.mylove.send(re.reply_name)

                    # 不论是否有响应都关闭前置功能
                    self.template.close_front_function()

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
        pass