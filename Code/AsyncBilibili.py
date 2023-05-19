import json
from Lib.AsyncNetwork import Network


class Bilibili():
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/"
    }

    def __init__(self, s=Network({}, log_level=30)) -> None:
        self.s = s
        self.s.changeHeader(self.header)

    # async def get(self, url):
    #     r = await self.s.get(url)
    #     return await r.json(content_type="application/json")

    async def get(self, url, tryMAX=1000):
        async def _get(tryID=0):
            tmp = await self.s.get(url)
            tmp = await tmp.json(content_type=None)
            if tryID >= tryMAX:
                return tmp
            if tmp["code"] != 0:
                tryID += 1
                return await _get(tryID)
            else:
                return tmp
        return await _get()

    async def videoshot(self, BV):
        "视频缩略图"
        url = f"https://api.bilibili.com/x/player/videoshot?bvid={BV}&index=1"
        return await self.get(url)

    async def videolist(self, UID, page=1):
        url = f"https://api.bilibili.com/x/space/wbi/arc/search?mid={UID}&ps=30&tid=0&pn={page}&keyword=&order=pubdate"
        return await self.get(url)

    async def videoinfo(self, BV):
        url = f"https://api.bilibili.com/x/web-interface/view/detail?platform=web&bvid={BV}"
        return await self.get(url)

    async def spaceInfo(self, UID):
        "个人空间信息"
        url = f"https://api.bilibili.com/x/space/acc/info?mid={UID}"
        return await self.get(url)

    async def DynamicList(self, UID, offset=""):
        '动态列表\n\noffset由上一个获取的列表提供'
        url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={offset}&host_mid={UID}&timezone_offset=-480&features=itemOpusStyle"
        return await self.get(url)

    async def LiveRoomID(self, UID):
        return await self.spaceInfo(UID)['data']['live_room']['roomid']

    async def LiveInfo(self, room_id):
        url = f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}"
        return await self.get(url)

    async def IsLiveNow(self, UID):
        tmp = await self.spaceInfo(UID)
        try:
            return tmp['data']['live_room']['liveStatus'] == 1
        except TypeError:
            return None  # 账户不存在直播间
        except KeyError:
            return None
