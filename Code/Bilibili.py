from Lib.Network import Network


class Bilibili():
    header = {
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/"
    }

    def __init__(self, s=Network({})) -> None:
        self.s = s
        self.s.changeHeader(self.header)

    def get(self, url):
        return self.s.get(url).json()

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
