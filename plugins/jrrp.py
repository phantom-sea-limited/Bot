from nonebot.adapters.mirai2.event import MessageEvent
from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot import on_keyword
import random
import time
from Lib.ini import CONF


jrrp_de = on_keyword(["今日人品", "人品", "jrrp"], priority=1, block=True)


@jrrp_de.handle()
async def __jrrp_de(event: MessageEvent):
    try:
        name = event.sender.name
    except Exception:
        name = event.sender.nickname
    c = CONF("jrrp")
    t = time.strftime("%Y-%m-%d", time.localtime())
    if c.load(str(event.sender.id), "day")[0] == t:
        if c.load(str(event.sender.id), "type")[0] == "jrrp":
            star = c.load(str(event.sender.id), "star")[0]
            await jrrp_de.finish(f"{name}今日会收到{star}颗星星！从月球直邮的哟")
        else:
            await jrrp_de.finish("今日人品和今日抽签只能二选一的说")
    else:
        star = random.randint(1, 100)
        c.add(str(event.sender.id), "type", "jrrp")
        c.add(str(event.sender.id), "star", star)
        c.add(str(event.sender.id), "day", t)
        c.save()
        await jrrp_de.finish(f"{name}今日会收到{star}颗星星！从月球直邮的哟")


jrrp_cq = on_keyword(["今日抽签", "抽签"], priority=1, block=True)


@jrrp_cq.handle()
async def __jrrp_cq(event: MessageEvent):
    try:
        name = event.sender.name
    except Exception:
        name = event.sender.nickname
    c = CONF("jrrp")
    t = time.strftime("%Y-%m-%d", time.localtime())
    if c.load(str(event.sender.id), "day")[0] == t:
        if c.load(str(event.sender.id), "type")[0] == "jrcq":
            star = c.load(str(event.sender.id), "star")[0]
            msg = MessageChain(MessageSegment.plain(f"{name}发现了了一个旧得发黄变脆的竹筒，\n你随手一摸\n") + MessageSegment.image(
                path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/order/{star}.png"))
            await jrrp_cq.finish(msg)
        else:
            await jrrp_cq.finish("今日人品和今日抽签只能二选一的说")
    else:
        star = random.randint(-3, 3)
        c.add(str(event.sender.id), "type", "jrcq")
        c.add(str(event.sender.id), "star", star)
        c.add(str(event.sender.id), "day", t)
        c.save()
        msg = MessageChain(MessageSegment.plain(f"{name}发现了了一个旧得发黄变脆的竹筒，\n你随手一摸\n") + MessageSegment.image(
            path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/order/{star}.png"))
        await jrrp_cq.finish(msg)
