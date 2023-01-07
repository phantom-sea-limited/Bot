import time
from nonebot.adapters.mirai2.event import MessageEvent
from Lib.ini import CONF


class Limit():
    def __init__(self, limit_time=60) -> None:
        self.t = limit_time

    async def limit(self, event: MessageEvent) -> bool:
        id = event.get_user_id()
        c = CONF("limit")
        t = time.time()
        ot = c.load(id, "t")[0]
        if ot == False:
            return True
        if float(ot) <= t:
            return True
        else:
            return False

    async def set(self, event: MessageEvent):
        id = event.get_user_id()
        c = CONF("limit")
        t = time.time()
        c.add(id, "t", t + self.t)
        c.save()
        return None
