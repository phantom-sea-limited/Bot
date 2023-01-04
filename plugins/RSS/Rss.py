from Lib.Network import Network
from urllib.parse import quote
from Lib.ini import CONF
import json


class RSS():
    sec = "RSS"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        self.s = n
        self.c = c

    def rss(self, url):
        return self.s.get(f"https://api.rss2json.com/v1/api.json?rss_url={quote(url)}")

    def cache(self, url, data: str = ""):
        if data == "":
            # 在ini无法输入%之前采用的暴力措施
            # return base64.b64decode(bytes(self.c.load(self.sec, quote(url))[0], encoding='utf-8')).decode()
            return self.c.load(self.sec, quote(url))[0]
        else:
            # self.c.add(self.sec, quote(url), base64.b64encode(data.encode('utf8')).decode())
            self.c.add(self.sec, quote(url), data)
            self.c.save()

    def subscribe(self, url):
        all = self.c.load(self.sec, "subscribe")[0]
        if all == False:
            all = []
        else:
            all = json.loads(all)
        if url not in all:
            all.append(url)
            self.c.add(self.sec, "subscribe", json.dumps(all))
            self.c.save()
            return True
        return False

    def unsubscribe(self, url):
        all = self.c.load(self.sec, "subscribe")[0]
        all = json.loads(all)
        try:
            all.remove(url)
        except Exception:
            return False
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

    def analysis(self, url):
        "重点重构对象,提取缓存与实时RSS订阅的内容区别,即更新的内容"
        return self.rss(url).json()

    def transform(self, data):
        "重点重构对象,将更新的条目整合成一条消息"
        return data


class Acgnx(RSS):
    sec = "Acgnx"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        super().__init__(n, c)

    def rss(self, word):
        url = f"https://share.acgnx.net/rss.xml?keyword={word}"
        return super().rss(url)

    def cache(self, word, data: json = {"items": [{"title": ""}]}):
        return super().cache(word, data["items"][0]["title"])

    def subscribe(self, word):
        return super().subscribe(word)

    def unsubscribe(self, word):
        return super().unsubscribe(word)

    def analysis(self, word):
        old = self.cache(word)
        new = self.rss(word).json()
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

    def transform(self, new: json):
        if new["items"] == []:
            return False
        msg = f"叮叮,侦测到订阅更新\n{new['feed']['title']}\n\n"
        for i in new["items"]:
            msg += f"{i['categories'][0]} {i['title']}\n{i['link'].replace('https://share.acgnx.se','https://share.acgnx.net')}\n\n"
        return msg[:-2]
