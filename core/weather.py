import datetime
import json
import random
import traceback

import requests
from requests import Timeout, HTTPError

import settings
import tool
from core import util
from core.log import Log
from model.text.template import TextTemplate
from settings import USER_AGENT
from lxml import etree

from tool.util import select_with_regex


class WeatherCatcher:

    url = "http://weather.sina.com.cn/hefei"

    url_home = "http://weather.sina.com.cn/haerbin"

    base_xpath = "//div[@id='blk_fc_c0_scroll']/div[2]/"

    @classmethod
    def weather_info_dict(cls):
        """
        返回抓取后的weather信息dict, 并写到天气信息文件中
        :return: info dict
        """
        # weather info dict
        di = cls._get_info_dict(str(cls._get_raw_html(), "utf-8"))

        with open(settings.WEATHER_PATH, "w") as f:
            f.write(json.dumps(di))

        return di

        pass

    @classmethod
    def _get_raw_html(cls):
        """
        返回原生天气html
        :return: bytes
        """

        try:
            ra = util.get_rand_number(0, len(USER_AGENT) - 1)

            # 根据假期得到响应的url
            if settings.TERM == 0 or settings.TERM == 2:
                r_url = cls.url
            else:
                r_url = cls.url_home

            resp = requests.get(url=r_url, headers={"User-Agent": USER_AGENT[ra]})

            # 判断抓去天气的情况
            if resp.status_code == 200:
                return resp.content

            pass
        except Timeout as timeout:
            Log.send_email(traceback.format_exc())

            pass
        except ConnectionError as ce:
            Log.send_email(traceback.format_exc())

            pass
        except HTTPError as he:
            Log.send_email(traceback.format_exc())

            pass
        except Exception as e:
            Log.send_email(traceback.format_exc())

            pass
        pass

    @classmethod
    def _get_info_dict(cls, raw_html):
        """
        解析原生html
        :param raw_html: 原生html
        :return: dict
        """
        parse = etree.HTML(raw_html)

        YEAR = datetime.datetime.now().strftime("%Y")

        # 日期
        date = YEAR + "-" + parse.xpath(cls.base_xpath + "p[@class='wt_fc_c0_i_date']/text()")[0]

        # 时间
        time = datetime.datetime.now().strftime("%H:%M:%S")

        # 星期
        week = parse.xpath(cls.base_xpath + "p[@class='wt_fc_c0_i_day ']/text()")[0]

        # 白天主要天气
        day_main_weather = parse.xpath(cls.base_xpath + "p[contains(@class, 'wt_fc_c0_i_icons')]/img[1]/@alt")[0]

        # 夜晚主要天气
        night_main_weather = parse.xpath(cls.base_xpath + "p[contains(@class, 'wt_fc_c0_i_icons')]/img[2]/@alt")[0]

        # 原生总天气
        sum_temperature = parse.xpath(cls.base_xpath + "p[@class='wt_fc_c0_i_temp']/text()")[0].replace(" ", '')

        # highest
        highest_temperature = select_with_regex("(.*)/.*", sum_temperature)

        # lowest
        lowest_temperature = select_with_regex(".*/(.*)", sum_temperature)

        # 空气指数
        air_condition_number = parse.xpath(cls.base_xpath + "ul[contains(@class, 'wt_fc_c0_i_level')]/li[@class='l']/text()")[0]

        # 空气指数描述
        air_condition_statement = parse.xpath(cls.base_xpath + "ul[contains(@class, 'wt_fc_c0_i_level')]/li[@class='r']/text()")[0]

        return {
            "time": date + " " + time,
            "week": week,
            "status": "success",
            "weather_data": {
                "day_main_weather": day_main_weather,
                "night_main_weather": night_main_weather,
                "highest_temperature": highest_temperature,
                "lowest_temperature": lowest_temperature,
                "air_condition_number": air_condition_number,
                "air_condition_statement": air_condition_statement
            }
        }

        pass
    pass


class WeatherSender:

    # 天气信息的评论
    inner_weather_comment_dict = {
        "day_main_weather": None,
        "temperature": None,
        "air_condition": None
    }

    @classmethod
    def send_weather(cls, little_sa):
        """
        发送已经抓取的天气信息
        :param little_sa: 小萨对象引用
        :return:None
        """

        weather_dict = cls._read_weather_info()

        cls._get_weather_comment(weather_dict)

        text_template = cls._get_weather_text_template()

        # 从str时间分离年月日
        now_date = tool.util.from_str_time_get_datetime(weather_dict["time"])

        # 格式化文字
        result = text_template % (str(now_date.year),
                                  str(now_date.month),
                                  str(now_date.day),
                                  weather_dict["week"],
                                  weather_dict["weather_data"]["day_main_weather"],
                                  cls.inner_weather_comment_dict["day_main_weather"],
                                  weather_dict["weather_data"]["night_main_weather"],
                                  weather_dict["weather_data"]["highest_temperature"],
                                  weather_dict["weather_data"]["lowest_temperature"],
                                  cls.inner_weather_comment_dict["temperature"],
                                  weather_dict["weather_data"]["air_condition_number"],
                                  weather_dict["weather_data"]["air_condition_statement"],
                                  cls.inner_weather_comment_dict["air_condition"])

        little_sa.mylove.send(result)

        return result
        pass

    @classmethod
    def _read_weather_info(cls):
        """
        获取抓取到本地的天气信息
        :return: dict
        """

        with open(settings.WEATHER_PATH, "r") as f:
            s = f.read()

        return json.loads(s)
        pass

    @classmethod
    def _get_weather_text_template(cls):
        """
        获取文字模版
        :return: str
        """

        text_list = TextTemplate.inner_dict["template"]["weather"]

        # 随机取模版中的一个
        rand_index = random.randint(0, len(text_list) - 1)

        return text_list[rand_index]
        pass

    @classmethod
    def _get_weather_comment(cls, weather_info_dict):
        """
        得到天气信息的评论
        :param weather_info_dict: 天气信息
        :return:
        """
        cls.inner_weather_comment_dict["day_main_weather"] = TextTemplate.from_main_weather_get_comment(
            weather_info_dict["weather_data"]["day_main_weather"])

        cls.inner_weather_comment_dict["temperature"] = TextTemplate.from_temperature_get_comment(
            weather_info_dict["weather_data"]["highest_temperature"],
            weather_info_dict["weather_data"]["lowest_temperature"])

        cls.inner_weather_comment_dict["air_condition"] = TextTemplate.from_air_get_comment(
            weather_info_dict["weather_data"]["air_condition_number"])

        pass
    pass

