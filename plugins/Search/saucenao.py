import nonebot
from Lib.Network import Network


driver = nonebot.get_driver()
key = getattr(driver.config, "saucenao", False)


class saucenao():
    def __init__(self, url) -> None:
        if key == False:
            raise KeyError
        self.url = url
        self.get()

    def get(self):
        url = f"https://saucenao.com/search.php?api_key={key}&db=999&output_type=2&testmode=1&numres=16&url={self.url}"
        n = Network({"saucenao.com":"104.26.1.232"})
        self.r = n.get(url).json()

    
    def analysis(self):
        pass


