from Lib.Network import Network


class Ex():
    def __init__(self, ip, ex=False, cookie=False) -> None:
        '''不对cookie的有效性进行校验，请自行确保cookie完全正确\n\ncookie基本常年不会变动'''
        if ex and cookie:
            self.url = "https://exhentai.org"
            self.s = Network(
                {
                    "exhentai.org": {
                        "ip": ip
                    }
                }
            )
        else:
            self.url = "https://e-hentai.org/"
            self.s = Network(
                {
                    "e-hentai.org": {
                        "ip": ip
                    }
                }
            )
        if cookie:
            self.s.changeHeader({"Cookie": cookie})

    def get(self, url):
        r = self.s.get(url=f"{self.url}{url}")
        return r

    def post(self, data):
        r = self.s.post(f"{self.url}api.php", json=data)
        return r

    @staticmethod
    def log(text):
        with open("ex.html", "w", encoding="utf-8") as f:
            f.write(text)

    @staticmethod
    def analysis(text, method):
        from bs4 import BeautifulSoup
        if method == "type":
            raw = BeautifulSoup(text, "lxml")
            Type = raw.find_all(id="gdc")
            return Type

    @classmethod
    def exbest(cls, ips: list = ["178.175.129.254", "178.175.132.20", "178.175.132.22", "178.175.128.252", "178.175.128.254", "178.175.129.252"], cookie=False):
        from .IPcheck import IPcheck
        result = IPcheck(ips, "exhentai.org").run()
        print(f"已选中最快IP:{result['ip']}")
        return cls(result["ip"], ex=True, cookie=cookie)

    @classmethod
    def ehbest(cls, ips: list = ["172.67.0.127", "104.20.135.21", "104.20.134.21"], cookie=False):
        from .IPcheck import IPcheck
        result = IPcheck(ips, "e-hentai.org").run()
        print(f"已选中最快IP:{result['ip']}")
        return cls(result["ip"], ex=False, cookie=cookie)

    @classmethod
    def best(cls, ex=False, cookie=False):
        if ex and cookie:
            return cls.exbest(cookie=cookie)
        else:
            return cls.ehbest(cookie=cookie)
