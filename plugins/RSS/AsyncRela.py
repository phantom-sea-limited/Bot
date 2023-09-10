from Lib.AsyncNetwork import Network
from Lib.ini import CONF
from .AsyncRss import RSS, RSSException


class RelaComic(RSS):
    # header = {
    #     "referer": "https://m.relamanhua.com/",
    #     "origin": "https://m.relamanhua.com",
    #     "accept": "application/json"
    # }
    API = "https://static.deception.world/https://api.relamanhua.com/api/v3/"
    sec = "RelaComic"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        "热辣漫画订阅"
        super().__init__(n, c)
        # self.s.changeHeader(self.header)

    async def rss(self, url):
        r = await self.s.get(self.API + url)
        return await r.json(content_type="")

    get = rss

    async def conf(self):
        url = "system/network2?format=json&platform=1"
        return await self.get(url)

    async def analysis(self, word):
        url = f"comic2/{word}?format=json&platform=1"
        new = await self.rss(url)
        uuid = new["results"]["comic"]["last_chapter"]["uuid"]
        self.DataMap(word, new["results"]["comic"]["name"])
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

    async def transform(self, data, msg="叮叮,侦测到热辣漫画更新\n"):
        if data == False:
            return False
        msg += f'{data["results"]["comic"]["name"]}\t作者 {data["results"]["comic"]["author"][0]["name"]}\n'
        msg += f'https://m.relamanhua.com/v2h5/comicContent/{data["results"]["comic"]["path_word"]}/{data["results"]["comic"]["last_chapter"]["uuid"]}'
        return msg

    async def search(self, word):
        url = f"search/comic?format=json&platform=1&q={word}&limit=20&offset=0&_update=true"
        r = await self.get(url)
        if r["results"]["list"] == []:
            return "什么都没搜到"
        else:
            msg = ""
            for i in r["results"]["list"]:
                msg += f'{i["name"]}\t作者 {i["author"][0]["name"]}\n订阅关键词\t{i["path_word"]}\n\n'
            return msg[:-2]

    async def TranslateID(self, ID):
        r = await self.rss(f"comic2/{ID}?format=json&platform=1")
        return r["results"]["comic"]["name"]

    def start(self):
        return [self.InitMAP]
