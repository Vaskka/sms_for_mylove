# -*- coding: utf-8 -*-
import time

import schedule

from core.main_core import LittleSa
from settings import DEBUG


def debug():
    """
    debug模式
    :return:
    """

    pass


def main_run():
    """
    线上模式
    :return:
    """

    m = LittleSa()
    m.init_sa()

    while True:
        schedule.run_pending()
        time.sleep(1)
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


if __name__ == '__main__':
    main()

    pass
