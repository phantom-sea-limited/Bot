from dataclasses import dataclass
from nonebot import on_startswith
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.mirai2.event import MessageEvent
from nonebot_plugin_apscheduler import scheduler
from Lib.AsyncBot import BOT
from Lib.Message import Message
from .AsyncRss import *


@dataclass
class Rss:
    keyword: str
    handle: RSS


SUB = (
    Rss("acgnx", Acgnx()),
    Rss("热辣漫画", RelaComic())
)


def handles():
    def run(a: Rss):
        def get_id(event: MessageEvent):
            try:
                return event.sender.group.id, "sendGroupMessage"
            except Exception:
                return event.sender.id, "sendFriendMessage"

        async def _subscribe(matcher: Matcher, event: MessageEvent):
            word = event.get_plaintext().replace(a.keyword + "订阅", "")
            id, type = get_id(event)
            if word != "":
                r = a.handle.subscribe(
                    {"word": word, "target": id, "type": type})
            else:
                r = False
            if r:
                try:
                    await a.handle.analysis(word)
                except RSSException as e:
                    await matcher.finish(e.args[0])
                await matcher.finish("订阅成功")
            else:
                await matcher.finish("订阅失败,订阅已存在或其他原因")

        async def _unsubscribe(matcher: Matcher, event: MessageEvent):
            word = event.get_plaintext().replace(a.keyword + "取消订阅", "")
            id, type = get_id(event)
            if word != "":
                r = a.handle.unsubscribe(
                    {"word": word, "target": id, "type": type})
            else:
                r = False
            if r:
                await matcher.finish("取消订阅成功")
            else:
                await matcher.finish("取消订阅失败,订阅不存在或其他原因")

        async def _showsubscribe(matcher: Matcher, event: MessageEvent):
            id = get_id(event)[0]
            r = a.handle.showsubscribe()
            fin = []
            for i in r:
                if i["target"] == int(id):
                    fin.append(i["word"])
            if fin == []:
                await matcher.finish(f"关于{a.keyword}的订阅为空")
            msg = f"关于{a.keyword}的订阅如下\n"
            for i in fin:
                msg += f"{i}\n"
            await matcher.finish(msg[:-1])

        async def _fetchsubscribe():
            r = a.handle.showsubscribe()
            if r == []:
                pass
            else:
                for i in r:
                    msg = await a.handle.analysis(i["word"])
                    msg = a.handle.transform(msg)
                    logger.info(i["word"] + "\t" + str(msg))
                    if msg != False:
                        m = Message(i["target"])
                        m.plain(msg)
                        r = await BOT(a.handle.s).sendMessage(m.get_message(), i["type"])
                        logger.info(str(r))

        async def _search(matcher: Matcher, event: MessageEvent):
            word = event.get_plaintext().replace(a.keyword + "搜索", "")
            r = await a.handle.search(word)
            if r == None:
                await matcher.finish(a.keyword + "搜索功能未启用")
            else:
                await matcher.finish(r)

        return _subscribe, _unsubscribe, _showsubscribe, _fetchsubscribe, _search

    for i in SUB:
        subscribe, unsubscribe, showsubscribe, fetchsubscribe, search = run(i)
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
        on_startswith(
            i.keyword + "搜索", priority=1, block=True
        ).append_handler(search)
        scheduler.add_job(fetchsubscribe, trigger="cron",
                          hour="*/1", minute="30")
        timer = i.handle.Timer()
        if timer == []:
            pass
        else:
            for j in timer:
                scheduler.add_job(j["function"], trigger="cron",
                                  hour=j["cron"]["hour"], minute=j["cron"]["minute"])


handles()
