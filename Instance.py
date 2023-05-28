from nonebot import get_driver
from Lib.AsyncBot import BOT
from Lib.AsyncNetwork import Network
from Lib.AsyncProxyNetwork import Network as ProxyNetwork
from Code.AsyncPixiv import Pixiv

driver = get_driver()
# Audio
FFMPEG = getattr(driver.config, "ffmpeg", False)
# PIXIV
PHPSESSID = getattr(driver.config, "pixiv_phpsessid", "")
MIRROR = getattr(driver.config, "mirror", "piv.deception.world")
# BOT-HTTP-API
BotUrl = getattr(driver.config, "http_url", "http://127.0.0.1:20000/")
Master = getattr(driver.config, "http_master", "")
qq = getattr(driver.config, "http_qq", "")


class PixivInstance(Pixiv):
    Mirror = MIRROR

    def __init__(self, s=...) -> None:
        super().__init__(s, PHPSESSID)


class BOTInstance(BOT):
    BASE = BotUrl
    MASTER = Master
    QQ = qq


NetworkInstance = Network({})
ProxyNetworkInstance = ProxyNetwork({})
BOTInstanceInstance = BOTInstance(NetworkInstance)
