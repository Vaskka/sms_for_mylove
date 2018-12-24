import json

import schedule

from model import main_model
from model.main_model import AutoCheck


class Task:
    def __init__(self, *args, **kwargs):
        """
        任务类，包含定时任务执行的时刻，定时执行的函数
        """
        # name
        self.name = kwargs["name"]

        # 定时执行的函数
        self.job = kwargs["job"]

        # 定时执行的时间
        self.do_at = kwargs["at"]

        # 描述
        self.statement = kwargs["statement"]
        pass

    pass


class Timer:
    def __init__(self, task_path):
        """
        定时执行类
        :param task_path 任务配置文件路径
        """

        # 定时执行的任务队列
        self.task_queue = []

        # 配置文件路径
        self.path = task_path

        with open(task_path, "r") as f:
            list_str = f.read()

        # task dict list
        self.task_list = json.loads(list_str)

        pass

    def do_register(self):
        """
        注册全部Task
        :return:
        """

        for task_setting in self.task_list:
            t = Task(name=task_setting["name"],
                     at=task_setting["at"],
                     job=getattr(main_model, task_setting["do_model_class"]).run,
                     statement=task_setting["statement"])
            self._register_task(t)
            pass

        # 默认检查任务
        self._register_task(Task(name='auto_check', at="1:00", job=AutoCheck.run, statement='inner check'))

        pass

    def _register_task(self, task):
        """
        将任务注册在任务队列
        :param task: 任务
        :return:
        """
        # 注册在任务队列
        self.task_queue.append(task)

        # 注册在schedule
        schedule.every().day.at(task.do_at).do(task.job)
        pass

    def task_queue_size(self):
        """
        返回任务队列的大小
        :return: int
        """
        return len(self.task_queue)

        pass

    def show_current_tasks(self):
        """
        拿到当前全部的task debug or log
        :return: str
        """
        result = "=============Task Queue=============\n"

        for task in self.task_queue:
            result += ("name:" + task.name + "\n")
            result += ("at:" + task.do_at + "\n")
            result += ("job:" + task.job.__code__ + "\n")
            result += "-------------------------------\n"
            pass

        result += "=====================================\n"

        return result
        pass

    pass
