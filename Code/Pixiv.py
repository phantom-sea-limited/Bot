from Lib.Network import Network


class Pixiv():
    "https://sirin.coding.net/public/api/Pixiv/git/files/master/method.py"

    header = {
        "Host": "www.pixiv.net",
        "referer": "https://www.pixiv.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
    }
    Mirror = "piv.deception.world"

    def __init__(self, s=Network({"www.pixiv.net": {"ip": "210.140.92.193"}}), PHPSESSID="") -> None:
        '''
        PHPSESSID为登录后Cookie中名为PHPSESSID的对应值\t请登录后按F12打开开发者工具寻找\n
        可以选择不登录,即保持为空,但是获取到的数据会有一定时间的延后(Pixiv官方的锅)\n
        目前找不到不登录不出现延时的API
        '''
        self.s = s
        self.header["Cookie"] = f"PHPSESSID={PHPSESSID}"
        self.s.changeHeader(header=self.header)

    def get(self, url, **kwargs):
        r = self.s.get(url, **kwargs)
        return r.json()

    # def dns(self):
    #     url = "https://1.1.1.1/dns-query?name=www.pixiv.net&type=A"
    #     return self.get(
    #         url, headers={"Accept": "application/dns-json"}, noDefaultHeader=True)

    def notification(self):
        url = "https://www.pixiv.net/ajax/notification"
        return self.get(url)

    def check_login_state(self) -> bool:
        r = self.notification()
        return r["error"] == False

    def get_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}"
        return self.get(url)

    def geturls_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}/pages"
        return self.get(url)

    def get_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/top?lang=zh"
        return self.get(url)

    def get_by_Nid(self, NoverID):
        url = f"https://www.pixiv.net/ajax/novel/{NoverID}?lang=zh"
        return self.get(url)
