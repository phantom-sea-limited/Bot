from nonebot import get_driver
from Lib.AsyncBot import BOT
from Code.AsyncPixiv import Pixiv

driver = get_driver()
PHPSESSID = getattr(driver.config, "pixiv_phpsessid", "")
BotUrl = getattr(driver.config, "http_url", "http://127.0.0.1:20000/")
Master = getattr(driver.config, "http_master", "")
qq = getattr(driver.config, "http_qq", "")


class PixivInstance(Pixiv):
    def __init__(self, s=...) -> None:
        super().__init__(s, PHPSESSID)


class BOTInstance(BOT):
    BASE = BotUrl
    MASTER = Master
    QQ = qq
