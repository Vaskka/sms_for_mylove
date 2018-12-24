import datetime

import settings
from core import util


class Checker:
    """
    自动检查
    当前功能检查学期是否需要变化 每年的7月17日 9月{first-Monday}日 1月17日 3月{first-Monday}日
    """

    @classmethod
    def do_check(cls):
        """
        进行检查
        :return: str
        """
        now = datetime.datetime.now()

        axis_March = datetime.datetime(now.year, 3, util._get_first_monday_in_month(3))

        axis_September = datetime.datetime(now.year, 9, util._get_first_monday_in_month(9))

        if settings.TERM == 0 and now.month == 7 and now.day == 17:
            settings.TERM = 3
        elif settings.TERM == 1 and now.month == 3 and now.day == axis_March.day:
            settings.TERM = 0
        elif settings.TERM == 2 and now.month == 1 and now.day == 17:
            settings.TERM = 1
        elif settings.TERM == 3 and now.month == 9 and now.day == axis_September.day:
            settings.TERM = 2

        return "当前是" + settings.TERM_STD_DICT[settings.TERM]
        pass
    pass
