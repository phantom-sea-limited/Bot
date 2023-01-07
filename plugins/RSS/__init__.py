from dataclasses import dataclass
from nonebot import on_startswith
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.mirai2.event import Event
from nonebot_plugin_apscheduler import scheduler
from Lib.AsyncBot import BOT
from Lib.Message import Message
from .AsyncRss import *


@dataclass
class Rss:
    keyword: str
    handle: RSS
    target: int


SUB = (
    Rss("acgnx", Acgnx(), 960290056),
)


def handles():
    def run(a: Rss):
        async def _subscribe(matcher: Matcher, event: Event):
            word = event.get_plaintext().replace(a.keyword + "订阅", "")
            if word != "":
                r = a.handle.subscribe(word)
            else:
                r = False
            if r:
                await a.handle.analysis(word)
                await matcher.finish("订阅成功")
            else:
                await matcher.finish("订阅失败,订阅已存在或其他原因")

        async def _unsubscribe(matcher: Matcher, event: Event):
            word = event.get_plaintext().replace(a.keyword + "取消订阅", "")
            if word != "":
                r = a.handle.unsubscribe(word)
            else:
                r = False
            if r:
                await matcher.finish("取消订阅成功")
            else:
                await matcher.finish("取消订阅失败,订阅不存在或其他原因")

        async def _showsubscribe(matcher: Matcher):
            r = a.handle.showsubscribe()
            if r == []:
                await matcher.finish(f"关于{a.keyword}的订阅为空")
            msg = f"关于{a.keyword}的订阅如下\n"
            for i in r:
                msg += f"{i}\n"
            await matcher.finish(msg[:-1])

        async def _fetchsubscribe():
            r = a.handle.showsubscribe()
            if r == []:
                pass
            else:
                for i in r:
                    msg = await a.handle.analysis(i)
                    msg = a.handle.transform(msg)
                    logger.info(i + "\t" + str(msg))
                    if msg != False:
                        m = Message(a.target)
                        m.plain(msg)
                        r = await BOT(a.handle.s).sendMessage(m.get_message(), "sendGroupMessage")
                        logger.info(str(r))

        return _subscribe, _unsubscribe, _showsubscribe, _fetchsubscribe

    for i in SUB:
        subscribe, unsubscribe, showsubscribe, fetchsubscribe = run(i)
        on_startswith(
            i.keyword + "订阅", priority=2, block=True
        ).append_handler(subscribe)
        on_startswith(
            i.keyword + "取消订阅", priority=2, block=True
        ).append_handler(unsubscribe)
        on_startswith(
            i.keyword + "订阅列表", priority=1, block=True
        ).append_handler(showsubscribe)
        on_startswith(
            [i.keyword + "更新订阅", i.keyword + "订阅更新"], priority=1, block=True
        ).append_handler(fetchsubscribe)
        scheduler.add_job(fetchsubscribe, trigger="cron",
                          hour="*/1", minute="30")


handles()
