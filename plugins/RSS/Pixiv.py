import json
from Lib.Network import Network
from Lib.ini import CONF
from .Rss import RSS


class Pixiv(RSS):
    "https://sirin.coding.net/public/api/Pixiv/git/files/master/method.py"

    header = {
        "Host": "www.pixiv.net",
        "referer": "https://www.pixiv.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
    }
    Mirror = "piv.deception.world"
    sec = "Pixiv"

    def __init__(self, n=Network({"www.pixiv.net": {"ip": "210.140.92.193"}}), c=CONF("rss"), PHPSESSID="") -> None:
        '''
        PHPSESSID为登录后Cookie中名为PHPSESSID的对应值\t请登录后按F12打开开发者工具寻找\n
        可以选择不登录,即保持为空,但是获取到的数据会有一定时间的延后(Pixiv官方的锅)\n
        目前找不到不登录不出现延时的API
        '''
        super().__init__(n, c)
        self.header["Cookie"] = f"PHPSESSID={PHPSESSID}"
        self.s.changeHeader(header=self.header)

    def get(self, url, **kwargs):
        r = self.s.get(url, **kwargs)
        return r.json()

    def get_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}"
        return self.get(url)

    def geturls_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}/pages"
        return self.get(url)

    def get_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/top?lang=zh"
        return self.get(url)

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
        return fin

    def cache(self, uid, data: str = ""):
        if data == "":
            return json.loads(super().cache(str(uid), ""))
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
        for i in data:
            print(i)
