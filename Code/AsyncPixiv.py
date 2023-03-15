from Lib.AsyncNetwork import Network


class Pixiv():
    "https://sirin.coding.net/public/api/Pixiv/git/files/master/method.py"

    header = {
        "Host": "www.pixiv.net",
        "referer": "https://www.pixiv.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
    }
    Mirror = "piv.deception.world"
    Logined = False
    "登录设置"

    def __init__(self, s=Network({"www.pixiv.net": {"ip": "210.140.92.193"}}), PHPSESSID="") -> None:
        '''
        PHPSESSID为登录后Cookie中名为PHPSESSID的对应值\t请登录后按F12打开开发者工具寻找\n
        可以选择不登录,即保持为空,但是获取到的数据会有一定时间的延后(Pixiv官方的锅)\n
        目前找不到不登录不出现延时的API
        '''
        self.s = s
        if PHPSESSID != "":
            self.header["Cookie"] = f"PHPSESSID={PHPSESSID}"
            self.Logined = True
        self.s.changeHeader(header=self.header)

    async def get(self, url, **kwargs):
        r = await self.s.get(url, **kwargs)
        return await r.json()

    # def dns(self):
    #     url = "https://1.1.1.1/dns-query?name=www.pixiv.net&type=A"
    #     return self.get(
    #         url, headers={"Accept": "application/dns-json"}, noDefaultHeader=True)

    async def notification(self):
        url = "https://www.pixiv.net/ajax/notification"
        return await self.get(url)

    async def check_login_state(self) -> bool:
        "登录正常返回True"
        r = await self.notification()
        return r["error"] == False

    async def check_logined_state(self) -> bool:
        "登录状态匹配设置返回True"
        r = await self.check_login_state()
        return r == self.Logined

    async def get_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}"
        return await self.get(url)

    async def geturls_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}/pages"
        return await self.get(url)

    async def get_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/top?lang=zh"
        return await self.get(url)

    async def get_all_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/all?lang=zh"
        return await self.get(url)

    async def get_by_Nid(self, NoverID):
        url = f"https://www.pixiv.net/ajax/novel/{NoverID}?lang=zh"
        return await self.get(url)
