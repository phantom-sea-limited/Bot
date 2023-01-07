import xmltodict
from Lib.Network import Network
from Lib.ini import CONF
from .Rss import *


class RssTest(RSS):
    '''Rss备用替换母版,使用xmltodict取代API'''

    sec = "RssTest"

    def __init__(self, n=Network({}), c=CONF("rss")) -> None:
        super().__init__(n, c)

    def rss(self, url):
        r = self.s.get(url)
        r.json = self.json
        self.r = r
        return r

    def json(self):
        return xmltodict.parse(self.r.text)
