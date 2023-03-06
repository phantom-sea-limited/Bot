import json
from copy import deepcopy
from Lib.Network import Network
from Lib.ini import CONF
from .Rss import RSS, RSSException


class Qidian(RSS):
    sec = "Qidian"
    hour = "*"
    minute = "*/10"
    # header = {
    #     "user-agent": r'''Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.63''',
    #     "sec-ch-ua-platform": '''"Android"''',
    #     "sec-ch-ua-mobile": "?1",
    #     "cache-control": "max-age=0",
    #     "sec-fetch-dest": "document",
    #     "sec-fetch-mode": "navigate",
    #     "sec-fetch-site": "same-origin",
    #     "sec-fetch-user": "?1",
    #     "sec-ch-ua": '''"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"'''
    # }
    csrf_url = "https://m.qidian.com/book/1036370336/745977837.html"
    err = False

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        "起点小说订阅"
        super().__init__(n, c)
        # self.s.changeHeader(self.header)
        try:
            self.csrfToken()
        except:
            self.analysis = self.none

    def get(self, url):
        return self.s.get(url)

    def fetch(self, ID):
        url = f"https://m.qidian.com/majax/book/category?_csrfToken={self.csrf}&bookId={ID}"
        r = self.get(url).json()
        if r["code"] == 1:
            self.analysis = self.none
            self.err = True
            raise RSSException("警告,起点订阅模块csrfToken异常,请联系开发者修复")
        elif r["code"] == 1006:
            raise RSSException("获取资讯失败:你这书?它保真吗?")
        return self.filter(r)

    def none(self, **kwargs):
        "垃圾桶函数"
        if self.err == False:
            self.err = True
            raise RSSException("警告,起点订阅模块csrfToken获取异常,请联系开发者修复")
        return ""

    def csrfToken(self):
        r = self.get(self.csrf_url)
        self.csrf = r.headers.get(
            "set-cookie").split(";")[0].split("=")[1]
        return self.csrf

    @staticmethod
    def filter(data):
        fin = {
            "bookName": data["data"]["bookName"],
            "bookId": data["data"]["bookId"],
            "chapter": []
        }
        for i in data["data"]["vs"]:
            fin["chapter"].append({
                "vN": i["vN"],
                "lastChapterName": i["cs"][-1]["cN"],
                "lastChapterID": i["cs"][-1]["id"]
            })
        return fin

    def cache(self, uid, data: str = ""):
        if data == "":
            tmp = super().cache(str(uid), "")
            if tmp == False:
                return False
            else:
                return json.loads(tmp)
        return super().cache(str(uid), json.dumps(data))

    def analysis(self, ID):
        old = self.cache(ID)
        new = self.fetch(ID)
        out = deepcopy(new)
        if old == False:  # 初始化订阅
            self.cache(ID, new)
            return False
        else:
            self.cache(ID, new)
            for i in new["chapter"]:
                if i in old["chapter"]:
                    out["chapter"].remove(i)
            return out

    def transform(self, data, msg="噔↑噔噔↓噔↑\n"):
        if data == False:
            return False
        elif data["chapter"] == []:
            return False
        else:
            msg += f"《{data['bookName']}》更新咯~\n"
            for i in data["chapter"]:
                msg += i["vN"] + " " + i["lastChapterName"]
                msg += f"\nhttps://m.qidian.com/book/{data['bookId']}/{i['lastChapterID']}.html\n\n"
            return msg[:-2]
