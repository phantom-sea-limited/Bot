from .log import Log
import aiohttp
import traceback
import ssl
ssl_ctx = ssl.SSLContext()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

dfheader = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39",
    "sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"''',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "dnt": "1",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "utf-8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
}


def get_qs(qs, key):
    try:
        id = qs[key]
    except KeyError:
        return False
    else:
        return id


class Network():
    dfheader = dfheader.copy()

    def __init__(self, hostTips: dict, log_path=".log", log_level=20, proxies={"http": None, "https": None}) -> None:
        '''
        hostTips = {
            "office.com": {
                "ip": "0.0.0.0"
            },
            "office.com": {
                "ip": False
            }
        }
        '''

        self.LOG = Log("Network", log_level=log_level, log_path=log_path)
        # self.s.trust_env = False
        self.table = hostTips
        self.s = None

    async def session(self):
        if self.s is None:
            connector = aiohttp.TCPConnector(ssl=ssl_ctx)
            self.s = aiohttp.ClientSession(connector=connector)
            self.s.keep_alive = False
        return self.s

    async def get(self, url, headers=False, noDefaultHeader=False, changeDefaultHeader=False, verify=False, **kwargs):
        h = Header.headerchange(self, headers, noDefaultHeader, changeDefaultHeader)
        s = await self.session()
        domain = url.split("/")[2]
        conf = get_qs(self.table, domain)
        if conf != False:
            ip = get_qs(conf, "ip")
            if ip:
                url = url.replace(domain, ip)
                h["host"] = domain
        try:
            # async with s.get(url, headers=h, **kwargs) as r:
            #     await r.text(errors="ignore")
            r = await s.get(url, headers=h, **kwargs)
            # r = await s.get(url, headers=h, **kwargs)
            # await r.close()
        except Exception as e:
            self.LOG.error(f"[GET][ERROR]\t\t{url}\t{domain}\t{e.args}")
            raise Exception(e.args)
        self.LOG.info(f"[GET][INFO]\t\t{int(r.status)}\t{r.url}\t{domain}")
        try:
            self.LOG.debug(
                f"[GET][DEBUG]\t\t{h}\n"+"\t"*11 + f"{r.headers}\n" + "\t"*11 + f"{await r.text()}")
        except Exception:
            pass
        return r

    async def post(self, url, data=False, json={}, headers=False, noDefaultHeader=False, changeDefaultHeader=False, verify=False, **kwargs):
        h = Header.headerchange(self, headers, noDefaultHeader, changeDefaultHeader)
        s = await self.session()
        domain = url.split("/")[2]
        conf = get_qs(self.table, domain)
        if conf != False:
            ip = get_qs(conf, "ip")
            if ip:
                url = url.replace(domain, ip)
                h["host"] = domain
        try:
            if data == False:
                # async with s.post(url, json=json, headers=h,
                #                   **kwargs) as r:
                #     await r.text(errors="ignore")
                r = await s.post(url, json=json, headers=h, **kwargs)
                data = json
            else:
                # async with s.post(url, data=data, headers=h,
                #                   **kwargs) as r:
                r = await s.post(url, data=data, headers=h, **kwargs)
                # await r.text(errors="ignore")
        except Exception as e:
            self.LOG.error(
                f"[POST][ERROR]\t\t{url}\t{domain}\t{data}\t{json}\t{e.args}\n{traceback.format_exc()}")
            raise Exception(e.args)
        self.LOG.info(f"[POST][INFO]\t\t{int(r.status)}\t{r.url}\t{domain}")
        try:
            self.LOG.debug(
                f"[POST][DEBUG]\t\t{h}\n"+"\t"*11 + f"{r.headers}\n" + "\t"*11 + f"{data}\n" + "\t"*11 + f"{await r.text()}")
        except Exception:
            pass
        return r

    def put(self, url, data=False, json={}, headers=False, noDefaultHeader=False, changeDefaultHeader=False, verify=False, **kwargs):
        h = Header.headerchange(self, headers, noDefaultHeader, changeDefaultHeader)
        domain = url.split("/")[2]
        conf = get_qs(self.table, domain)
        if conf != False:
            ip = get_qs(conf, "ip")
            if ip:
                url = url.replace(domain, ip)
                h["host"] = domain
        try:
            if data == False:
                r = self.s.put(url, json=json, headers=h,
                               verify=False, **kwargs)
                data = json
            else:
                r = self.s.put(url, data=data, headers=h,
                               verify=False, **kwargs)
        except Exception as e:
            self.LOG.error(f"[POST][ERROR]\t\t{url}\t{domain}\t{e.args}\n{traceback.format_exc()}")
            raise Exception(e.args)
        self.LOG.info(f"[POST][INFO]\t\t{r.status}\t{r.url}\t{domain}")
        try:
            self.LOG.debug(
                f"[POST][DEBUG]\t\t{h}\n"+"\t"*11 + f"{r.headers}\n" + "\t"*11 + f"{data}\n" + "\t"*11 + f"{r.text}")
        except Exception:
            pass
        return r

    def changeHeader(self, header, noDefaultHeader=False):
        return Header.headerchange(self, header, noDefaultHeader, changeDefaultHeader=True)


class Header():
    @staticmethod
    def headerchange(N: Network, header, noDefaultHeader=False, changeDefaultHeader=False):
        if header:
            if noDefaultHeader:
                h = header
            else:
                h = Header.addheader(N.dfheader, header)
        else:
            h = N.dfheader.copy()
        if changeDefaultHeader:
            N.dfheader = h.copy()
        return h

    @staticmethod
    def addheader(d1: dict, d2: dict):
        d = d2.copy()
        for i in d1:
            d[i] = d1[i]
        return d
