import json
import time

import schedule

import core
import model
import settings
from core.main_core import LittleSa
from core.weather import WeatherCatcher
from settings import DEBUG
from timer.maker import Timer, Task
from model.main_model import *


def debug():
    """
    debug模式
    :return:
    """

    m = LittleSa()
    m.init_sa()

    while True:
        schedule.run_pending()
        time.sleep(1)

    pass


def main_run():
    """
    线上模式
    :return:
    """
    pass


def main():
    """
    主函数
    :return:
    """
    if DEBUG:
        debug()
    else:
        main_run()
    pass

"""

test

"""
def test_model():
    t = Timer(settings.TASK_SETTING_PATH)
    t.do_register()
    pass


if __name__ == '__main__':
    # main()
    #test_model()
    debug()
    pass
