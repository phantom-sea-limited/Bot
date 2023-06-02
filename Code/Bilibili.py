import json
from Lib.Network import Network


class Bilibili():
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/",
        # 打开一个隐私页面进入bilibili获取cookie，降低被拦截的风险
        # "cookie": "innersign=0; buvid3=733660AE-0684-34F3-767C-FAE9A2310E1000765infoc; i-wanna-go-back=-1; b_ut=7; b_lsid=C4E6CCC2_188610818C9; _uuid=4F8510551-EA810-109D3-546E-31014BDF10758700627infoc; FEED_LIVE_VERSION=V8; header_theme_version=undefined; buvid_fp=06b03cdb07c2cca98d5d745863edf5ae; home_feed_column=5; browser_resolution=1523-738; buvid4=80FBE09F-7B61-A803-0032-AE01DD89859901955-023052814-w+I3G1KJ8dGIBb1F8nPWgA%3D%3D; b_nut=1685255102",
        "user-agent": ''' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'''
    }

    def __init__(self, s=Network({})) -> None:
        self.s = s
        self.s.changeHeader(self.header)

    def crsf(self):
        r = self.s.get("https://www.bilibili.com/")
        cookies = ""
        for i in r.headers.get("set-cookie").split(", "):
            j = i.split("; ")[0]
            if "=" in j:
                cookies += j + "; "

        self.s.changeHeader({"cookie": cookies})

    def get(self, url, tryMAX=999):
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
