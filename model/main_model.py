import datetime
import json
import traceback

from core import weather, lesson, auto_check, greeting, news
from core.log import Log
from model.base import BaseModel
from tool import util


class Greeting(BaseModel):

    name = "greeting"

    @classmethod
    def run(cls):
        """
        早安问候
        :return:
        """
        try:
            result_text = greeting.Greeting.send_greeting(cls.little_sa)

            # 记录log
            Log.write_success(cls.name, result_text)
        except Exception:
            cls.deal_error_traceback_log_format_str()


class WeatherCatcher(BaseModel):

    name = "weather_catcher"

    @classmethod
    def run(cls):
        """
        抓取天气逻辑
        :return:
        """
        try:
            di = weather.WeatherCatcher.weather_info_dict()

            # 记录log
            Log.write_success(cls.name, json.dumps(di))
        except Exception:
            cls.deal_error_traceback_log_format_str()
    pass


class WeatherSender(BaseModel):

    name = "weather_sender"

    @classmethod
    def run(cls):
        """
        发送天气数据
        :return:
        """
        try:
            result_text = weather.WeatherSender.send_weather(cls.little_sa)

            # 记录log
            Log.write_success(cls.name, result_text)
        except Exception:
            cls.deal_error_traceback_log_format_str()


class Lesson(BaseModel):

    name = "lesson"

    @classmethod
    def run(cls):
        """
        发送lesson运行逻辑
        :return:
        """
        try:
            result_text = lesson.Lesson.send_lesson(cls.little_sa)

            # 记录log
            Log.write_success(cls.name, result_text)
        except Exception:
            cls.deal_error_traceback_log_format_str()

        pass


class News(BaseModel):

    name = "news"

    @classmethod
    def run(cls):
        """
        发送新闻
        :return: None
        """
        try:
            result_text = news.News.send_news(cls.little_sa)

            # 记录log
            Log.write_success(cls.name, result_text)
        except Exception:
            cls.deal_error_traceback_log_format_str()
        pass


class AutoCheck(BaseModel):

    name = "auto_check"

    @classmethod
    def run(cls):
        """
        默认检查model
        当前功能：
            检查是否变换学期settings.TERM
        :return:
        """
        try:
            result_text = auto_check.Checker.do_check()

            # 记录log
            Log.write_success(cls.name, result_text)
        except Exception:
            cls.deal_error_traceback_log_format_str()

        pass

        pass
