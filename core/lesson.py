# -*- coding: utf-8 -*-
import datetime

import pymysql

import settings
from core.util import get_today_week_num
from model.text import template


class Lesson:

    @classmethod
    def send_lesson(cls, little_sa):
        """
        发送lesson信息
        :param little_sa: 小萨引用
        :return: str 课程信息
        """
        lesson_list = cls.from_database_get_lesson()

        if len(lesson_list) == 0:
            text = template.TextTemplate.get_lesson_text_template(False)
            little_sa.mylove.send(text % "")
            return text % ""
        else:
            text = template.TextTemplate.get_lesson_text_template(True)

        lesson_text = ""
        for d in lesson_list:
            r_text = "第" + str(d["num"]) + "节:\n"
            r_text += ("课程名:" + d["lesson_name"] + "\n")
            r_text += ("教室:" + d["classroom"] + "\n")
            r_text += "==================\n"

            lesson_text += r_text

        little_sa.mylove.send(text % lesson_text)
        return text % lesson_text
        pass

    @classmethod
    def from_database_get_lesson(cls):
        """
        从数据库获取今天全部课程
        :return: dict_list
        """
        # 数据库连接
        db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DATABASE)
        cursor = db.cursor()

        # 确定星期
        weekday = datetime.datetime.now().weekday()

        # 确定周次
        weeknum = get_today_week_num()

        sql = """
            select num, lesson_name, classroom from lesson where weekday=%d and weeknum=%d order by num;
        """ % (weekday, weeknum)

        cursor.execute(sql)
        results = cursor

        r_list = list()
        for result in results:
            d = dict()
            d["num"] = result[0]
            d["lesson_name"] = result[1]
            d["classroom"] = result[2].replace(" ", "")

            r_list.append(d)
            pass

        db.close()
        return r_list
    pass
