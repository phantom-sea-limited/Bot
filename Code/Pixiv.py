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
        self.s = s
        self.s.changeHeader(header=self.header)

    def get(self, url, **kwargs):
        r = self.s.get(url, **kwargs)
        return r.json()

    # def dns(self):
    #     url = "https://1.1.1.1/dns-query?name=www.pixiv.net&type=A"
    #     return self.get(
    #         url, headers={"Accept": "application/dns-json"}, noDefaultHeader=True)

    def get_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}"
        return self.get(url)

    def geturls_by_pid(self, pid):
        url = f"https://www.pixiv.net/ajax/illust/{pid}/pages"
        return self.get(url)

    def get_by_uid(self, uid):
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/top?lang=zh"
        return self.get(url)
