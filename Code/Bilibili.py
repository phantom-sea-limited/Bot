import json
from Lib.Network import Network


class Bilibili():
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/"
    }

    def __init__(self, s=Network({})) -> None:
        self.s = s
        # self.s.changeHeader(self.header)

    def get(self, url, tryMAX=1000):
        def _get(tryID=0):
            tmp = self.s.get(url).json()
            if tryID >= tryMAX:
                return tmp
            if tmp["code"] != 0:
                tryID += 1
                return _get(tryID)
            else:
                return tmp
        return _get()

    def videoshot(self, BV):
        "视频缩略图"
        url = f"https://api.bilibili.com/x/player/videoshot?bvid={BV}&index=1"
        return self.get(url)

    def videolist(self, UID, page=1):
        url = f"https://api.bilibili.com/x/space/wbi/arc/search?mid={UID}&ps=30&tid=0&pn={page}&keyword=&order=pubdate"
        return self.get(url)

    def videoinfo(self, BV):
        url = f"https://api.bilibili.com/x/web-interface/view/detail?platform=web&bvid={BV}"
        return self.get(url)

    def spaceInfo(self, UID):
        "个人空间信息"
        url = f"https://api.bilibili.com/x/space/acc/info?mid={UID}"
        return self.get(url)

    def DynamicList(self, UID, offset=""):
        '动态列表\n\noffset由上一个获取的列表提供'
        url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={offset}&host_mid={UID}&timezone_offset=-480&features=itemOpusStyle"
        return self.get(url)

    def LiveRoomID(self, UID):
        return self.spaceInfo(UID)['data']['live_room']['roomid']

    def LiveInfo(self, room_id):
        url = f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}"
        return self.get(url)

    def IsLiveNow(self, UID):
        try:
            return self.spaceInfo(UID)['data']['live_room']['liveStatus'] == 1
        except TypeError:
            return None  # 账户不存在直播间
        except KeyError:
            return None
