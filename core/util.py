# -*- coding: utf-8 -*-
import datetime
import random

import settings


def get_rand_number(min_n, max_n):
    """
    [min, max]
    :return: int
    """
    return random.randint(min_n, max_n)
    pass


def _get_first_monday_in_month(month):
    """
    得到某月的第一个星期一的日期
    :param month:
    :return: int 日期
    """

    # 今年年份
    year = datetime.datetime.now().strftime("%Y")

    # 拿到当前一号的情况
    first = datetime.datetime(int(year), month, 1)

    if first.weekday() == 0:
        return 1

    return int(datetime.datetime(int(year), month, 1 + 7 - first.weekday()).strftime("%d"))

    pass


def _get_now_axis_date():
    """
    得到这学期计算用轴 处于假期返回 None
    :return: datetime
    """
    # 今年年份
    year = int(datetime.datetime.now().strftime("%Y"))

    # 判断轴
    if settings.TERM == 0:
        return datetime.datetime(year, 3, _get_first_monday_in_month(3))
    elif settings.TERM == 2:
        return datetime.datetime(year, 9, _get_first_monday_in_month(9))
    else:
        return None
    pass


def get_today_week_num():
    """
    得到今天的周次
    :return: 周次
    """

    axis_date = _get_now_axis_date()

    # 假期返回None
    if axis_date is None:
        return None

    now_date = datetime.datetime.now()

    days = (now_date - axis_date).days

    return int(days / 7) + 1

