from PIL import Image
from io import BytesIO
import requests
import argparse


class SFEAutoCheckIn:
    def __init__(self, cookies):
        self.cookies = cookies
        self.headers = {
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            "cookie": self.cookies,
            "referer": "https://sfe.simpfun.cn/point.php?&action=sign",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-des": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }

    def get_checkin_image(self) -> BytesIO:
        """
        :return: (BytesIO) 服务器返回签到图片的字节流
        """
        url = "https://sfe.simpfun.cn/sign_code/tncode.php"
        res = requests.get(url, headers=self.headers)
        byte_stream = BytesIO(res.content)
        return byte_stream

    def cut_picture(self):
        """
        :return: (Image) 缺口图片, (Image) 完整图片
        """
        bs = self.get_checkin_image()
        image = Image.open(bs)
        piece_image = image.crop((0, 0, 240, 150))
        full_image = image.crop((0, 300, 240, 450))
        return piece_image, full_image

    def get_distance(self, bg_image, full_image):
        """
        :param bg_image: (Image)缺口图片
        :param full_image: (Image)完整图片
        :return: (Int)缺口离滑块的距离
        """
        # 滑块的初始位置
        distance = 50
        # 遍历像素点横坐标
        for i in range(distance, full_image.size[0]):
            # 遍历像素点纵坐标
            for j in range(full_image.size[1]):
                # 如果不是相同像素
                if not self.is_pixel_equal(full_image, bg_image, i, j):
                    # 返回此时横轴坐标就是滑块需要移动的距离
                    return i

    def is_pixel_equal(self, bg_image, fullbg_image, x, y):
        """
        :param bg_image: (Image)缺口图片
        :param fullbg_image: (Image)完整图片
        :param x: (Int)位置x
        :param y: (Int)位置y
        :return: (Boolean)像素是否相同
        """
        # 获取缺口图片的像素点(按照RGB格式)
        bg_pixel = bg_image.load()[x, y]
        # 获取完整图片的像素点(按照RGB格式)
        full_pixel = fullbg_image.load()[x, y]
        # 设置一个判定值，像素值之差超过判定值则认为该像素不相同
        threshold = 50
        # 判断像素的各个颜色之差，abs()用于取绝对值
        if abs(bg_pixel[0] - full_pixel[0] < threshold) and abs(bg_pixel[1] - full_pixel[1] < threshold) and abs(
                bg_pixel[2] - full_pixel[2] < threshold):
            # 如果差值在判断值之内，返回是相同像素
            return True
        else:
            # 如果差值在判断值之外，返回不是相同像素
            return False

    def post_answer(self, result):
        """
        :param result: (Int) 缺口偏移值
        :return: (String) 签到语句
        """
        url = "https://sfe.simpfun.cn/sign_code/check.php"
        payload = {
            "tn_r": result
        }
        resp = requests.post(url, data=payload, headers=self.headers)
        return resp.text

    def run(self):
        piece, full = self.cut_picture()
        result = self.get_distance(piece, full)
        return self.post_answer(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prefix_chars="-", description="简幻欢平台过人机验证")
    parser.add_argument('-c', '--cookies', help="用户的cookies，可以在浏览器通过开发者工具查看", type=str, action="store")
    user_cookies = parser.parse_args().cookies
    print(SFEAutoCheckIn(user_cookies).run())
