import time
from nonebot.adapters.mirai2.event import MessageEvent
from Lib.ini import CONF

c = CONF("limit")


class Limit():
    def __init__(self, limit_time=60, channel="defalut") -> None:
        self.t = limit_time
        self.channel = channel

    async def limit(self, event: MessageEvent) -> bool:
        id = event.get_user_id()
        t = time.time()
        ot = c.load(self.channel, id)[0]
        if ot == False:
            return True
        if float(ot) <= t:
            return True
        else:
            return False

    async def set(self, event: MessageEvent):
        id = event.get_user_id()
        t = time.time()
        c.add(self.channel, id, t + self.t)
        c.save()
        return None
