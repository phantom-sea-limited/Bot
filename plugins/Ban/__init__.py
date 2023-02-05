from nonebot import on_type
from nonebot.matcher import Matcher
from nonebot.adapters.mirai2.event import GroupMessage
from .list import *

_BAN = on_type(GroupMessage, priority=1, block=False)


LIST = [img]


@_BAN.handle()
async def _(matcher: Matcher, event: GroupMessage):
    for i in LIST:
        try:
            if await i.check(matcher, event):
                await i.function(matcher, event)
        except Exception:
            pass
