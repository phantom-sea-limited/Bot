import json
from Lib.Network import Network
from Lib.ini import CONF
from Lib.Message import MesssagePart
from Code.Pixiv import Pixiv
from .Rss import RSS, RSSException


class PixivRSS(RSS, Pixiv):
    sec = "Pixiv"

    def __init__(self, n=Network({"www.pixiv.net": {"ip": "210.140.92.193"}}), c=CONF("rss"), PHPSESSID="") -> None:
        RSS.__init__(self, n, c)
        Pixiv.__init__(self, n, PHPSESSID)

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

    def analysis(self, uid):
        new = self.get_by_uid(uid)
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

    def transform(self, data, msg="叮叮,侦测到订阅更新\n"):
        msg = MesssagePart.plain(msg)
        if data["illusts"] != []:
            i = data["illusts"][0]
            r = self.get_by_pid(i)
            msg += MesssagePart.plain(
                f'PID\t{i}\n{r["body"]["illustTitle"]}')
            msg += MesssagePart.image(r["body"]["urls"]
                                        ["original"].replace("i.pximg.net", self.Mirror))
            if len(data["illusts"]) > 1:
                msg += MesssagePart.plain(f'\n\n更多更新请查看https://www.pixiv.net/users/{r["body"]["userId"]}')
        if data["manga"] != []:
            for i in data["manga"]:
                pass
        if data["novels"] != []:
            for i in data["novels"]:
                msg += MesssagePart.plain(i)
