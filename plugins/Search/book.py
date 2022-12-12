from Lib.AsyncNetwork import Network
from nonebot.log import logger

BASE = "https://api.phantom-sea-limited.ltd/release/API/search/"
BASE2 = "https://service-av2jrwkk-1258642780.hk.apigw.tencentcs.com/release/API/get?id="


class BOOK():
    def __init__(self, s=Network({})) -> None:
        self.s = s

    async def Graph(self, word, start, end):
        try:
            URL = BASE + f"Graph?wd={word}&api"
            r = await self.s.get(URL).json()
            i = start - 1
            fin = ""
            while i < end:
                fin += f'''{i+1}.{r["value"][i]["name"]}\n{BASE2}{r["value"][i]["id"]}\n\n'''
                i += 1
            return fin[:-2]
        except Exception:
            import traceback
            logger.error(traceback.format_exc())
            return "搜索结果被吞了,留下了500的字样"

    async def Sharepoint(self, word, start, end):
        try:
            URL = BASE + f"Sharepoint?wd={word}&api"
            r = await self.s.get(URL).json()
            i = start - 1
            fin = ""
            while i < end:
                fin += f'''{i+1}.{r["value"][i]["name"]}\n{BASE2}{r["value"][i]["id"]}\n\n'''
                i += 1
            return fin[:-2]
        except Exception:
            import traceback
            logger.error(traceback.format_exc())
            return "搜索结果被吞了,留下了500的字样"
