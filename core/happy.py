import pymysql

import settings


class Happy:

    @classmethod
    def send_happy(cls, little_sa):
        """
        发送每日笑笑
        :param little_sa: 小萨引用
        :return: None
        """
        result_text = cls._get_happy_str()
        little_sa.mylove.send(result_text)

        return result_text

        pass

    @classmethod
    def _get_happy_str(cls):
        """
        得到每日笑笑的发送信息
        :return: str
        """
        db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DATABASE)
        cursor = db.cursor()

        sql = """
            SELECT joke_content FROM joke WHERE id >= ((SELECT MAX(id) FROM joke)-(SELECT MIN(id) FROM joke)) * RAND() + (SELECT MIN(id) FROM joke)  LIMIT 1;
        """

        cursor.execute(sql)
        results = cursor

        result_str = "今天的每日笑笑😋:\n"

        for result in results:
            result_str += result[0]

        return result_str + "\n(可能不会很好笑啦，主人说以后会找更好的笑话资源的～小萨会继续努力哒!)"
        pass
