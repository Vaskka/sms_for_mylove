# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import settings
from settings import EMAIL_TO, EMAIL_SUBJECT
from tool import util


class Log:
    """
    捕获异常
    """

    @classmethod
    def send_email(cls, content):
        """
        发送异常
        :return: None
        """
        ret = True
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = formataddr(["Vaskka", '1139851358@qq.com'])
            msg['To'] = formataddr(["Vaskka", EMAIL_TO])
            msg['Subject'] = EMAIL_SUBJECT

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login('1139851358@qq.com', 'tfbzouaytwscfjfg')
            server.sendmail('1139851358@qq.com', [EMAIL_TO, ], msg.as_string())
            server.quit()  # quit
        except Exception:
            ret = False

        return ret
        pass

    @classmethod
    def write_in_log(cls, content):
        """
        写入log
        :param content:
        :return:
        """
        content += "\n"
        if not os.path.exists(settings.LOG_PATH):
            with open(settings.LOG_PATH, "w") as f:
                f.write(content)
        else:
            with open(settings.LOG_PATH, "a") as f:
                f.write(content)

        pass

    @classmethod
    def write_success(cls, name, success_content):
        """
        写入成功调用的log
        :param name: model名称
        :param success_content: 成功调用的信息
        :return: None
        """

        cls.write_in_log("[success]" + util.get_now_datetime() + "--" + name + "--" + success_content)
        pass
    pass