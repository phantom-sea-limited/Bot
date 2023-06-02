from nonebot import get_driver
from Lib.AsyncBot import BOT
from Lib.AsyncNetwork import Network
from Lib.AsyncProxyNetwork import Network as ProxyNetwork
from Code.AsyncPixiv import Pixiv
from Code.AsyncBilibili import Bilibili

driver = get_driver()
# Audio
FFMPEG = getattr(driver.config, "ffmpeg", False)
# PIXIV
PHPSESSID = getattr(driver.config, "pixiv_phpsessid", "")
MIRROR = getattr(driver.config, "mirror", "piv.deception.world")
# BILIBILI
BILICOOKIE = getattr(driver.config, "bilicookie", "")
# BOT-HTTP-API
BotUrl = getattr(driver.config, "http_url", "http://127.0.0.1:20000/")
Master = getattr(driver.config, "http_master", "")
qq = getattr(driver.config, "http_qq", "")


class PixivInstance(Pixiv):
    Mirror = MIRROR

    def __init__(self, s=...) -> None:
        super().__init__(s, PHPSESSID)


class BiliInstance(Bilibili):
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/",
        "cookie": BILICOOKIE,
        "user-agent": ''' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'''
    }


class BOTInstance(BOT):
    BASE = BotUrl
    MASTER = Master
    QQ = qq


NetworkInstance = Network({})
ProxyNetworkInstance = ProxyNetwork({})
BOTInstanceInstance = BOTInstance(NetworkInstance)
