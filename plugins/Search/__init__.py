from nonebot.adapters.mirai2.event import MessageEvent, GroupMessage
from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot import on_keyword
from .saucenao import saucenao

soutu = on_keyword(["搜图"], priority=5)


@soutu.handle()
async def __soutu():
    await soutu.finish('''搜图说明书:
请使用:(搜图+)[搜索源]+[图/回复一张图/稍后发送一张图]
目前已有搜索源:
    saucenao''')


saucenao = on_keyword(["搜图 saucenao", "saucenao"], priority=5)


@saucenao.handle()
async def __saucenao(event: GroupMessage):
    id = event.json()

    print(id)
