
# 调试模式
import os

DEBUG = False

# 学期 0-春季 1-寒假 2-秋季 3-暑假
TERM = 2

TERM_STD_DICT = {
    0: "春季",
    1: "寒假",
    2: "秋季",
    3: "暑假"
}

# 爬虫ua
USER_AGENT = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
]

# 异常邮件提醒配置
EMAIL_SUBJECT = "小萨生病了；；"
EMAIL_TO = "1139851358@qq.com"


# 天气信息文件路径
WEATHER_INFO_FILENAME = "weather.json"

# 定时任务配置文件路径
TASK_SETTING_PATH = "task.json"

# 文字模版配置文件
TEXT_TEMPLATE_SETTING_PATH = "text.json"

# mylove
MYLOVE_SENDER = "超喜欢的小糕哈哈哈"
# MYLOVE_SENDER = "Vernon"

# log文件路径
LOG_PATH = os.path.join(os.environ['HOME'], ".little_sa", "sa_log.log")

# .little_sa文件目录
POINT_MAIN_PATH = os.path.join(os.environ['HOME'], ".little_sa")

# 人脸框颜色对照
FACE_ATTR_RECT_COLOR = [
    {
        "rgb": (135, 206, 255),
        "name": "blue",
        "comment": "可爱蓝"
    },

    {
        "rgb": (144, 238, 144),
        "name": "green",
        "comment": "浅浅绿"
    },
    {
        "rgb": (125, 38, 205),
        "name": "purple",
        "comment": "深深紫"
    },
    {
        "rgb": (255, 255, 0),
        "name": "yellow",
        "comment": "柠檬黄"
    },
    {
        "rgb": (255, 105, 180),
        "name": "pink",
        "comment": "热情粉"
    }
]

# 情绪对照
FACE_EMOTION = {
    "sadness": "伤心",
    "disgust": "生气",
    "fear": "害怕",
    "happiness": "开心",
    "neutral": "淡定",
    "surprise": "惊讶"
}

# #### database #### #
# 数据库host
MYSQL_HOST = "localhost"
MYSQL_PASSWORD = "0000"
MYSQL_USER = "root"
MYSQL_DATABASE = "little_sa"

# 可用的功能
ENABLE_FUNCTION = {
    "greeting",
    "weather_catcher",
    "weather_sender",
    "lesson",
    "news",
    "face"
}

# # # API_KEY # # #

TULING_API_KEY = ""
FACE_API_KEY = ""
FACE_API_SECRET = ""
SHOW_API_KEY = ""