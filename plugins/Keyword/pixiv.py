from nonebot.adapters.mirai2.message import MessageSegment
from Instance import NetworkInstance as n


class Pixiv():
    @staticmethod
    async def random():
        r = await n.get(f"https://api.sirin.top/release/PIXIV/random")
        r = await r.json(content_type=None)
        return MessageSegment.plain(f'''PID {r["body"]["id"]}\n''') + MessageSegment.image(url=r["body"]["urls"]["original"].replace(
            "i.pixiv.re", "piv.deception.world"))
