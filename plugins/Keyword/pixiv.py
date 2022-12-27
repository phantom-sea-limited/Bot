from Lib.AsyncNetwork import Network
from nonebot.adapters.mirai2.message import MessageSegment


class Pixiv():
    @staticmethod
    async def random():
        n = Network({})
        r = await n.get(f"https://api.sirin.top/release/PIXIV/random")
        r = await r.json(content_type="text/json")
        return MessageSegment.plain(f'''PID {r["body"]["id"]}\n''') + MessageSegment.image(url=r["body"]["urls"]["original"].replace(
            "i.pixiv.re", "piv.deception.world"))
