import traceback

from wxpy import *

import settings
from core.log import Log
from tool import util


class BaseModel:

    # model name
    name = "base model"

    # 小萨饮引用
    little_sa = None

    @classmethod
    def run(cls):
        """
        模型运行函数，模型逻辑
        :return:
        """
        pass

    @classmethod
    def deal_error_traceback_log_format_str(cls):
        """
        记录本地log和发送异常邮件提醒
        :return: None
        """
        error_msg = traceback.format_exc()

        # 记录log
        Log.write_in_log("[error]" + util.get_now_datetime() + "--" + cls.name + "--" + error_msg)

        # trackback邮件提醒
        Log.send_email(error_msg)
    pass
