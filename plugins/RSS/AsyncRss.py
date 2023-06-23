import json
from urllib.parse import quote
from Lib.AsyncNetwork import Network
from Lib.ini import CONF


class RSS():
    sec = "RSS"
    hour = "*/1"
    minute = "30"
    wait = 5
    "订阅更新间隔"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        self.s = n
        self.c = c

    async def rss(self, url):
        return await self.s.get(f"https://api.rss2json.com/v1/api.json?rss_url={quote(url,'')}")

    def cache(self, url, data: str = ""):
        if data == "":
            # 在ini无法输入%之前采用的暴力措施
            # return base64.b64decode(bytes(self.c.load(self.sec, quote(url))[0], encoding='utf-8')).decode()
            return self.c.load(self.sec, quote(url))[0]
        else:
            # self.c.add(self.sec, quote(url), base64.b64encode(data.encode('utf8')).decode())
            self.c.add(self.sec, quote(url), data)
            # self.c.save()

    def subscribe(self, data):
        all = self.c.load(self.sec, "subscribe")[0]
        if all == False:
            all = []
        else:
            all = json.loads(all)
        if data not in all:
            all.append(data)
            self.c.add(self.sec, "subscribe", json.dumps(all))
            self.c.save()
            return True
        return False

    def unsubscribe(self, data):
        all = self.c.load(self.sec, "subscribe")[0]
        all = json.loads(all)
        try:
            all.remove(data)
        except Exception:
            return False
        self.c.remove(self.sec, data["word"])
        self.c.add(self.sec, "subscribe", json.dumps(all))
        self.c.save()
        return True

    def showsubscribe(self):
        all = self.c.load(self.sec, "subscribe")[0]
        if all == False:
            all = []
        else:
            all = json.loads(all)
        return all

    async def analysis(self, url):
        "重点重构对象,提取缓存与实时RSS订阅的内容区别,即更新的内容"
        return await self.rss(url).json()

    async def transform(self, data, msg=""):
        "重点重构对象,将更新的条目整合成一条消息,返回MesssagePart或其可兼容值"
        return data

    def Timer(self):
        '''需要定时器的功能,返回值为空列表或\n        
        [{
            "function": callable,
            "cron": {
                "hour": "*/12",
                "minute": "*"
            }
        }]'''
        return []

    def start(self):
        '''预加载的功能,返回值为空列表或\n        
        [callable1,callable2]'''
        return []

    async def search(self, word):
        "实现搜索功能,正常应该返回MessageChain或其可兼容值"


class RSSException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Acgnx(RSS):
    sec = "Acgnx"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        "末日動漫資源庫 - Project AcgnX Torrent Asia \nhttps://share.acgnx.net/"
        super().__init__(n, c)

    async def rss(self, word):
        url = f"https://share.acgnx.net/rss.xml?keyword={word.replace(' ','+')}"
        return await super().rss(url)

    def cache(self, word, data: json = {"items": [{"title": ""}]}):
        return super().cache(word, data["items"][0]["title"])

    async def analysis(self, word):
        old = self.cache(word)
        new = await self.rss(word)
        new = await new.json()
        if new["items"] == []:  # 获取内容为空,代表着未初始化
            self.cache(word, {"items": [{"title": []}]})
            return new
        if old == "[]":  # 缓存为空,获取内容不为空,即订阅更新
            self.cache(word, new)
            return new
        if old == False:  # 初始化订阅
            self.cache(word, new)
            new["items"] = []
            return new
        else:
            diff = []
            for i in new["items"]:
                if i["title"] == old:
                    self.cache(word, new)
                    new["items"] = diff
                    return new
                else:
                    diff.append(i)
            # 未能匹配到缓存中的更新时间,即长时间未获取更新,更新列表过长直接忽略
            self.cache(word, new)
            new["items"] = []
            return new

    async def transform(self, new: json, msg="叮叮,侦测到ACGNX更新\n"):
        if new["items"] == []:
            return False
        msg = f"{msg}{new['feed']['title']}\n\n"
        for i in new["items"]:
            msg += f"{i['categories'][0]} {i['title']}\n{i['link'].replace('https://share.acgnx.se','https://share.acgnx.net')}\n\n"
        return msg[:-2]

    async def search(self, word):
        if word == "":
            return "不能搜索虚空.jpg"
        r = await self.rss(word)
        r = await self.transform(await r.json(), "")
        if r == False:
            return "什么都没搜到"
        else:
            return r
