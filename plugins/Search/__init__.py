from nonebot.adapters.mirai2.event import MessageEvent, GroupMessage
from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot import on_keyword, on_startswith
from nonebot.matcher import Matcher

soutu = on_keyword(["搜图"], priority=5, block=True)


@soutu.handle()
async def __soutu():
    await soutu.finish('''搜图说明书:
请使用:(搜图+)[搜索源]+[图/回复一张图/稍后发送一张图]
目前已有搜索源:
    saucenao''')


saucenao = on_keyword(["搜图 saucenao", "saucenao"], priority=5, block=True)


@saucenao.handle()
async def __saucenao(event: GroupMessage):
    from .saucenao import saucenao
    id = event.json()

    print(id)


sousuo = on_startswith(["搜索"], priority=5, block=True)


@sousuo.handle()
async def _sousuo(matcher: Matcher, event: GroupMessage):
    msg = event.get_message().extract_plain_text().replace("搜索", "")
    if msg == "":
        await matcher.finish("虚空搜索来咯")
    else:
        from .book import BOOK
        b = BOOK()
        fin = await b.Graph(msg, 1, 5)
        await matcher.finish(fin)