import asyncio
import traceback
from dataclasses import dataclass
from nonebot import on_startswith, get_driver
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.mirai2.event import MessageEvent
from nonebot.adapters.mirai2.message import MessageChain
from nonebot_plugin_apscheduler import scheduler
from Instance import BOTInstanceInstance as BOT
from Instance import NetworkInstance
from Lib.Message import Message
from Lib.ini import CONF
from .AsyncRss import *
from .AsyncRela import RelaComic
from .AsyncPixiv import PixivRSS
from .AsyncQidian import Qidian
from .AsyncBilibili import BiliRss

Driver = get_driver()

MAXError = 5


@dataclass
class Rss:
    keyword: str
    handle: RSS
    updating: bool = False
    error: int = 0


c = CONF("rss")

SUB = (
    Rss("acgnx", Acgnx(NetworkInstance, c=c)),
    Rss("热辣漫画", RelaComic(NetworkInstance, c=c)),
    Rss("pixiv", PixivRSS(c=c)),
    Rss("起点", Qidian(NetworkInstance, c=c)),
    Rss("b站", BiliRss(c=c))
)


def handles():

    def save():
        for i in SUB:
            if i.updating:
                logger.info("RSS未保存")
                return None
        c.save()
        logger.info("RSS已保存")

    def run(a: Rss):
        def get_id(event: MessageEvent):
            try:
                return event.sender.group.id, "sendGroupMessage"
            except Exception:
                return event.sender.id, "sendFriendMessage"

        async def _subscribe(matcher: Matcher, event: MessageEvent):
            word = event.get_plaintext().replace(a.keyword + "订阅", "")
            id, type = get_id(event)
            if word == "":
                await matcher.finish("虚空订阅?")
            try:
                await a.handle.analysis(word)
            except RSSException as e:
                await matcher.finish(e.args[0])
            r = a.handle.subscribe(
                {"word": word, "target": id, "type": type})
            if r:
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
            r = a.handle.showrawsubscribe()
            for i in r:
                if a.error <= MAXError:
                    await asyncio.sleep(a.handle.wait)
                    try:
                        a.updating = True
                        msg = await a.handle.analysis(i["word"])
                        msg = await a.handle.transform(msg)
                        a.updating = False
                        save()
                    except RSSException as e:
                        a.updating = False
                        msg = e.args[0]
                        a.error += 1
                    except Exception as e:
                        a.updating = False
                        a.error += 1
                        msg = f"{a.keyword}订阅出现异常,异常计数{a.error}"
                        logger.error(
                            f"{a.keyword}订阅出现异常:\n{e.args}\n{traceback.format_exc()}")
                    logger.info(i["word"] + "\t" + str(msg))
                    if msg != False:
                        m = Message(i["target"])
                        m.input(msg)
                        r = await BOT.sendMessage(m.get_message(), i["type"])
                        logger.info(str(r))

        async def _search(matcher: Matcher, event: MessageEvent):
            word = event.get_plaintext().replace(a.keyword + "搜索", "")
            try:
                r = await a.handle.search(word)
            except RSSException as e:
                await matcher.finish(e.args[0])
            if r == None:
                await matcher.finish(a.keyword + "搜索功能未启用")
            else:
                await matcher.finish(MessageChain(r))

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
                          hour=i.handle.hour, minute=i.handle.minute)
        timer = i.handle.Timer()
        if timer == []:
            pass
        else:
            for j in timer:
                scheduler.add_job(j["function"], trigger="cron",
                                  hour=j["cron"]["hour"], minute=j["cron"]["minute"])
        start = i.handle.start()
        if start == []:
            pass
        else:
            for j in start:
                Driver.on_bot_connect(j)

    async def Status(matcher: Matcher, event: MessageEvent):
        msg = "订阅状态\n"
        for i in SUB:
            msg += i.keyword
            if i.error:
                msg += f"\t异常计数{i.error}\n"
            else:
                msg += "\t正常\n"
        await matcher.finish(msg[:-1])

    on_startswith(
        "订阅状态", priority=1, block=True
    ).append_handler(Status)


handles()
