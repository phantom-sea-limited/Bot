import time
import re
import json
from Lib.ini import CONF
from Lib.Network import Network
from Lib.ProxyNetwork import Network as Proxy


class BiliCookie():
    "https://socialsisteryi.github.io/bilibili-API-collect/docs/login/cookie_refresh.html"
    cookies = {}
    ac_time_value = None

    def __init__(self, p=Proxy({}), n=Network({}), c=CONF("bili")) -> None:
        self.n = n
        self.p = p
        self.c = c

    def Init(self, cookies, ac_time_value):
        if self.c.load("main", "cookie")[0] != cookies:
            self.c.add("main", "cookie", cookies)
            cookies = self.c.load("main", "cookie")[0]
            cookies = "{\"" + cookies.replace(";", "\",\"").replace(
                "=", "\":\"").replace(" ", "") + "\"}"
            self.cookies = json.loads(cookies)
            for i in self.cookies:
                self.c.add("cookie", str(i), self.cookies[i])
                self.cookies[i] = self.cookies[i]
                self.c.add("cookie", "all", json.dumps(
                    list(self.cookies.keys())))
        else:
            all = self.c.load("cookie", "all")[0]
            all = json.loads(all)
            for i in all:
                self.cookies[i] = self.c.load("cookie", i)[0]
        if self.c.load("main", "ac_time_value")[0] != ac_time_value:
            self.ac_time_value = ac_time_value
            self.c.add("main", "ac_time_value", ac_time_value)
            self.c.add("set", "ac_time_value", ac_time_value)
        else:
            self.ac_time_value = self.c.load("set", "ac_time_value")[0]

        self.c.save()

    def getCookie(self):
        cookies = ""
        for i in self.cookies:
            cookies += f"{i}={self.cookies[i]}; "
        return cookies[:-1]

    def checkAuth(self):
        r = self.n.get("https://passport.bilibili.com/x/passport-login/web/cookie/info",
                       headers={"cookie": f"SESSDATA={self.cookies['SESSDATA']}"})
        return r.json()

    def CorrespondPath(self, t=int(time.time()*1000)):
        r = self.p.get(
            f"https://wasm-rsa.vercel.app/api/rsa?t={t}")
        return r.json()["hash"]

    def refresh_csrf(self, CorrespondPath=""):
        if CorrespondPath == "":
            CorrespondPath = self.CorrespondPath()
        r = self.n.get(f"https://www.bilibili.com/correspond/1/{CorrespondPath}",
                       headers={"cookie": f"SESSDATA={self.cookies['SESSDATA']}"})
        if r.status_code == 200:
            return re.findall(r'<div id="1-name">([\s\S]+?)</div>', r.text)[0]
        else:
            return self.refresh_csrf()

    def RenewCookie(self, refresh_csrf=""):
        if refresh_csrf == "":
            refresh_csrf = self.refresh_csrf()
        # r = self.n.post("https://passport.bilibili.com/x/passport-login/web/cookie/refresh",
        #                 data=f"csrf={self.cookies['bili_jct']}&refresh_csrf={refresh_csrf}&source=main_web&refresh_token={self.ac_time_value}",
        #                 headers={"content-type": "application/x-www-form-urlencoded", "cookie": f"SESSDATA={self.cookies['SESSDATA']}"})
        r = self.n.post("https://passport.bilibili.com/x/passport-login/web/cookie/refresh",
                        data={
                            "csrf": self.cookies['bili_jct'],
                            "refresh_csrf": refresh_csrf,
                            "refresh_token": self.ac_time_value,
                            "source": "main_web",
                        }, headers={"content-type": "application/x-www-form-urlencoded", "cookie": self.getCookie()})
        fin = r.json()
        if (fin["code"] == 0):
            new = r.headers['Set-Cookie'].replace(" ", "").split(",")
            for i in new:
                if "=" in i:
                    j = i.split(";")[0].split("=")
                    self.cookies[j[0]] = j[1]
                    self.c.add("cookie", j[0], j[1])
            self.ac_time_value = fin["data"]["refresh_token"]
            self.c.add("set", "ac_time_value", fin["data"]["refresh_token"])
            self.c.save()
        return r

    def close(self):
        '缺失一种方法,用于过期旧的凭据'
