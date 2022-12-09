from nonebot.adapters.mirai2.event import MessageEvent
from Lib.ini import CONF
import time


class Limit():
    def __init__(self, limit_time=60) -> None:
        self.t = limit_time

    async def limit(self, event: MessageEvent) -> bool:
        id = event.get_user_id()
        c = CONF("limit")
        t = time.time()
        ot = c.load(id, "t")[0]
        if ot == False:
            c.add(id, "t", t + self.t)
            c.save()
            return True
        if float(ot) <= t:
            c.add(id, "t", t + self.t)
            c.save()
            return True
        else:
            return False
