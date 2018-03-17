# -*- coding: utf-8 -*-
# @Time    : 2018/3/17 15:01
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : code.py
# @Software: PyCharm

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
import uuid


# 定义验证码的功能
class Codes:
    # 随机一个字母或者数字
    def random_chr(self):
        num = random.randint(1, 3)
        if num == 1:
            # 随机一个0~9之间的数字
            char = random.randint(48, 57)  # asii码，0-9两端分别对应48,57
        elif num == 2:
            # 随机一个a~z之间的字母
            char = random.randint(97, 122)
        else:
            # 随机一个A~Z的字母
            char = random.randint(65, 90)
        return chr(char)

    # 随机加入干扰字符
    def random_dis(self):
        arr = ["^", "_", "~", "-", "."]
        return arr[random.randint(0, len(arr) - 1)]

    # 定义干扰字符的颜色,三原色，RGB，0~255
    def random_color1(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 定义字符的颜色
    def random_color2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 生成验证码
    def create_code(self):
        width = 240
        height = 60
        # 创建一个图片
        image = Image.new("RGB", (width, height), (192, 192, 192))
        # 创建font对象，定义字体和大小
        font_name = random.randint(1, 3)
        font_file = os.path.join(os.path.dirname(__file__), "static/fonts") + "/%d.ttf" % font_name
        font = ImageFont.truetype(font_file, 30)  # 路径以及大小
        # 创建一个draw对象，填充像素点
        draw = ImageDraw.Draw(image)
        for x in range(0, width, 5):
            for y in range(0, height, 5):
                draw.point((x, y), fill=self.random_color1())
        # 填充干扰字符
        for v in range(0, width, 30):  # 每间隔30个像素，填充一个字符
            dis = self.random_dis()
            w = 5 + v
            # 距离图片上边距最多15个像素，最低5个像素
            h = random.randint(5, 15)
            draw.text((w, h), dis, font=font, fill=self.random_color1())

        # 填充字符
        chars = ""
        for v in range(4):
            c = self.random_chr()
            chars += str(c)
            # 随机距离图片上边距离高度，最高15px，最低5px
            h = random.randint(5, 15)
            # 占图片宽度1/4，10px间隙
            w = width / 4 * v + 10
            draw.text((w, h), c, font=font, fill=self.random_color2())

        # 模糊效果
        image.filter(ImageFilter.BLUR)
        # 保存code图片
        # 保证唯一性
        image_name = "%s.jpg" % uuid.uuid4().hex

        save_dir = os.path.join(os.path.dirname(__file__), "static/code")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        image.save(save_dir + '/' + image_name, "jpeg")
        return dict(
            img_name=image_name,
            code=chars
        )
