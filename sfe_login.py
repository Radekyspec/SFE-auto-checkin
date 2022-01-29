import requests
import time


class SFELogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://sfe.simpfun.cn",
            "referer": "https://sfe.simpfun.cn/login.html",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }

    def login(self):
        """
        登录模块
        :return: (String) 使用账号密码登录获得cookies
        """
        url = "https://sfe.simpfun.cn/login-redirect.php"
        payload = {
            "QQ": self.username,
            "pass": self.password,
        }
        resp = requests.post(url, data=payload, headers=self.login_headers)
        return resp.headers["set-cookie"]

    def run(self):
        raw_cookies = None
        try:
            raw_cookies = self.login()
        except KeyError:
            error_count = 0
            while error_count <= 40:
                print("login error, retrying...")
                error_count += 1
                time.sleep(3)
                try:
                    raw_cookies = self.login()
                except KeyError:
                    error_count += 1
                else:
                    break
        return raw_cookies.split(';')[0]
