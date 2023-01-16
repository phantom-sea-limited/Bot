import json
from urllib.parse import quote
from Lib.Network import Network
from Lib.ini import CONF


class RSS():
    sec = "RSS"
    hour = "*/1"
    minute = "30"

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

    def analysis(self, url):
        "重点重构对象,提取缓存与实时RSS订阅的内容区别,即更新的内容"
        return self.rss(url).json()

    def transform(self, data, msg=""):
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

    def search(self, word):
        "实现搜索功能,正常应该返回MessageChain或其可兼容值"


class RSSException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Acgnx(RSS):
    sec = "Acgnx"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        super().__init__(n, c)

    def rss(self, word):
        url = f"https://share.acgnx.net/rss.xml?keyword={word}"
        return super().rss(url)

    def cache(self, word, data: json = {"items": [{"title": ""}]}):
        return super().cache(word, data["items"][0]["title"])

    def analysis(self, word):
        old = self.cache(word)
        new = self.rss(word).json()
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

    def transform(self, new: json, msg="叮叮,侦测到订阅更新\n"):
        if new["items"] == []:
            return False
        msg = f"{msg}{new['feed']['title']}\n\n"
        for i in new["items"]:
            msg += f"{i['categories'][0]} {i['title']}\n{i['link'].replace('https://share.acgnx.se','https://share.acgnx.net')}\n\n"
        return msg[:-2]

    def search(self, word):
        return self.transform(self.rss(word), msg="")


class RelaComic(RSS):
    header = {
        "referer": "https://m.relamanhua.com/",
        "origin": "https://m.relamanhua.com",
        "accept": "application/json"
    }
    API = "https://api.relamanhua.com/api/v3/"
    sec = "RelaComic"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        super().__init__(n, c)
        self.s.changeHeader(self.header)

    def rss(self, url):
        return self.s.get(self.API + url).json()

    get = rss

    def conf(self):
        url = "system/network2?platform=1"
        return self.get(url)

    def analysis(self, word):
        url = f"comic2/{word}?platform=1"
        new = self.rss(url)
        uuid = new["results"]["comic"]["last_chapter"]["uuid"]
        if new["code"] != 200:
            raise RSSException(new["message"])
        old = self.cache(word)
        if old == False:  # 初始化订阅
            self.cache(word, uuid)
            return False
        else:
            if old == uuid:
                return False
            else:
                self.cache(word, uuid)
                return new

    def transform(self, data, msg="叮叮,侦测到订阅更新\n"):
        if data == False:
            return False
        msg += f'{data["results"]["comic"]["name"]}\t作者 {data["results"]["comic"]["author"][0]["name"]}\n'
        msg += f'https://m.relamanhua.com/v2h5/comicContent/{data["results"]["comic"]["path_word"]}/{data["results"]["comic"]["last_chapter"]["uuid"]}'
        return msg

    def search(self, word):
        url = f"search/comic?platform=1&q={word}&limit=20&offset=0&_update=true"
        r = self.get(url)
        if r["results"]["list"] == []:
            return "什么都没搜到"
        else:
            msg = ""
            for i in r["results"]["list"]:
                msg += f'{i["name"]}\t作者 {i["author"][0]["name"]}\n订阅关键词\t{i["path_word"]}\n\n'
            return msg[:-2]
