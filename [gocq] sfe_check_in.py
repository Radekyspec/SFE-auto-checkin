import nonebot
import aiohttp
from ...utils import sfe_check_in
from ...utils import sfe_login
from bs4 import BeautifulSoup
from nonebot.adapters.onebot.v11.exception import ActionFailed

scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job('interval', minutes=2, max_instances=5)
async def auto_check_in():
    # 在这里填写你的账号和密码，以及你加入的聊天群群号~
    # 在这里填写你的账号和密码，以及你加入的聊天群群号~
    # 在这里填写你的账号和密码，以及你加入的聊天群群号~
    check_in_instance = CheckIn(username="", password="", group_id="")
    status = await check_in_instance.get_check_in_status()
    if status == "是":
        await check_in_instance.check_in()


class CheckIn:
    def __init__(self, username, password, group_id):
        self.username = username
        self.password = password
        self.group_id = group_id

    async def get_check_in_status(self):
        cookies = sfe_login.SFELogin(self.username, self.password).run()
        headers = {
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            "cookie": cookies,
            "referer": "https://sfe.simpfun.cn/index.php",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-des": "image",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        url = "https://sfe.simpfun.cn/point.php"
        payload = {
            "action": "sign"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=payload) as resp:
                resp = await resp.text()
        await session.close()

        soup = BeautifulSoup(resp, "html.parser")
        check_in_content = soup.find_all(name="td")[9]
        return str(check_in_content).split("<td>")[1].split("</td>")[0]

    async def check_in(self):
        bot = nonebot.get_bot()
        error_index = 0
        check_in_func = sfe_check_in.SFEAutoCheckIn(self.username, self.password)
        check_in_key = check_in_func.run()
        while check_in_key == "error" and error_index <= 20:
            nonebot.logger.error("Got an error from captcha, will try again soon")
            error_index += 1
            check_in_key = check_in_func.run()
        if error_index > 20:
            nonebot.logger.error("Error occurred when logging into SFR.")
        else:
            try:
                await bot.call_api(api="send_group_msg", **{"group_id": self.group_id, "message": check_in_key})
            except ActionFailed:
                await bot.call_api(api="send_group_msg", **{"group_id": self.group_id, "message": "刷新"})
        return
