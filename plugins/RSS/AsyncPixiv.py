import json
from nonebot.log import logger
from Lib.AsyncNetwork import Network
from Lib.ini import CONF
from Lib.Message import MesssagePart
from Instance import PixivInstance as Pixiv
from .AsyncRss import RSS, RSSException


class PixivRSS(RSS, Pixiv):
    sec = "Pixiv"
    hour = "*"
    minute = "*/20"
    err = False

    def __init__(self, n=Network({"www.pixiv.net": {"ip": "210.140.92.193"}}), c=CONF("rss")) -> None:
        RSS.__init__(self, n, c)
        Pixiv.__init__(self, n)

    async def none(self, **kwargs):
        "垃圾桶函数"
        if self.err == False:
            self.err = True
            raise RSSException("警告！pixiv登录状态失效，订阅系统已自动暂停，请修复后重启")
        return {'illusts': [], 'manga': [], 'novels': []}

    @staticmethod
    def top(data):
        fin = {
            "illusts": "",
            "manga": "",
            "novels": ""
        }
        if data["body"]["illusts"] != []:
            fin["illusts"] = list(data["body"]["illusts"].keys())[0]
        if data["body"]["manga"] != []:
            fin["manga"] = list(data["body"]["manga"].keys())[0]
        if data["body"]["novels"] != []:
            fin["novels"] = list(data["body"]["novels"].keys())[0]
        if fin == {"illusts": "", "manga": "", "novels": ""}:
            raise RSSException(
                f'订阅对象{data["body"]["extraData"]["meta"]["alternateLanguages"]["ja"]}所有数据都是空的，这是否有些问题？')
        return fin

    def cache(self, uid, data: str = ""):
        if data == "":
            tmp = super().cache(str(uid), "")
            if tmp == False:
                return False
            else:
                return json.loads(tmp)
        fin = self.top(data)
        return super().cache(str(uid), json.dumps(fin))

    async def check_logined_state(self) -> bool:
        if await super().check_logined_state() != True:
            self.analysis = self.none
            logger.error("Pixiv登录状态异常")
        else:
            logger.info("Pixiv登录状态正常")

    async def analysis(self, uid):
        new = await self.get_by_uid(uid)
        old = self.cache(uid)
        if old == False:  # 初始化订阅
            self.cache(uid, new)
            return False
        else:
            fin = {
                "illusts": [],
                "manga": [],
                "novels": []
            }
            for type in old:
                tmp = []
                if old[type] != []:  # 缓存不为空,正常判断
                    for i in new["body"][type]:
                        if i == old[type]:
                            fin[type] = tmp
                            break
                        else:
                            tmp.append(i)
                elif new["body"][type] != []:  # 缓存为空,更新不为空
                    for i in new["body"][type]:
                        tmp.append(i)
                    fin[type] = tmp
            self.cache(uid, new)
            return fin

    async def transform(self, data, msg="叮叮,侦测到订阅更新\n"):
        if data == {'illusts': [], 'manga': [], 'novels': []}:
            return False
        msg = MesssagePart.plain(msg)
        if data["illusts"] != []:
            i = data["illusts"][0]
            r = await self.get_by_pid(i)
            msg += MesssagePart.plain(
                f'PID {i}\n{r["body"]["illustTitle"]}')
            msg += MesssagePart.image(r["body"]["urls"]
                                      ["original"].replace("i.pximg.net", self.Mirror))
            msg += MesssagePart.plain(
                f'\n\n更多更新请查看https://www.pixiv.net/users/{r["body"]["userId"]}')
        if data["manga"] != []:
            i = data["manga"][0]
            msg += MesssagePart.plain(f"但是更新的是漫画，这部分功能尚未完成，漫画ID为{i}")
        if data["novels"] != []:
            i = data["novels"][0]
            msg += MesssagePart.plain(f"但是更新的是小说，这部分功能尚未完成，小说ID为{i}")
        return msg

    def Timer(self):
        return [{
            "function": self.check_logined_state,
            "cron": {
                "hour": "*",
                "minute": "30"
            }
        }]
