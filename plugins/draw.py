from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot import on_keyword

ability = on_keyword(["超能力"], priority=1, block=True)

@ability.handle()
async def __ability():
    await ability.finish("")