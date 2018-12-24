# -*- coding: utf-8 -*-
from model.text.template import TextTemplate


class Greeting:

    @classmethod
    def _get_greeting_str(cls):
        """
        得到问候信息
        :return: str
        """

        return TextTemplate.get_greeting_str()
        pass

    @classmethod
    def send_greeting(cls, little_sa):
        """
        发送问候信息
        :param little_sa: 小萨引用
        :return: str
        """

        g_msg = cls._get_greeting_str()

        little_sa.mylove.send(g_msg)
        return g_msg

    pass
