import datetime
import re

from PIL import Image, ImageDraw


def select_with_regex(regex, s, group=1):
    """
    利用正则提取str
    :param regex: 
    :param s: 
    :param group: 
    :return: 
    """
    result = re.match(regex, s)

    if result:
        return result.group(1)

    return None


def from_str_time_get_datetime(s_time):
    """
    从字符串时间得到datetime对象
    :param s_time: str 字符串时间
    :return: datetime
    """
    return datetime.datetime.strptime(s_time, "%Y-%m-%d %H:%M:%S")
    pass


def get_now_datetime():
    """
    得到当前时间str
    :return:
    """
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pass


def draw_rect_in_pic(path, rect, color):
    """
    在图片指定位置画指定颜色矩形（覆盖原图像）
    :param path: 图片位置
    :param rect: 矩形信息
    :param color: 颜色rgb-tuple
    :return: None
    """
    im = Image.open(path)
    draw = ImageDraw.Draw(im)

    draw.line(((rect["left"], rect["top"]), (rect["left"] + rect["width"], rect["top"])), width=2, fill=color)
    draw.line(((rect["left"] + rect["width"], rect["top"]), (rect["left"] + rect["width"], rect["top"] + rect["height"])), width=2, fill=color)
    draw.line(((rect["left"] + rect["width"], rect["top"] + rect["height"]), (rect["left"], rect["top"] + rect["height"])), width=2, fill=color)
    draw.line(((rect["left"], rect["top"] + rect["height"]), (rect["left"], rect["top"])), width=2, fill=color)

    im.save(path)
    pass


def is_valid_image(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False

    return bValid


def trans_img(img_path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    if is_valid_image(img_path):
        try:
            s = img_path.rsplit(".", 1)
            output_img_path = s[0] + ".jpg"
            im = Image.open(img_path)
            im.save(output_img_path)
            return True
        except:
            return False
    else:
        return False
