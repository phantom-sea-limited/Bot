from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot import on_keyword
from .__Limit import Limit

question = on_keyword(["???", "？？？"], priority=1, block=True)


@question.handle()
async def __question():
    await question.finish(MessageChain(MessageSegment.image(path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/chat/question.png")))

kill = on_keyword(["刑啊", "枪毙", "枪决", "击毙"], priority=1, block=True)


@kill.handle()
async def __kill():
    await kill.finish(MessageChain(MessageSegment.image(path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/chat/kill.png")))


setu = on_keyword(["涩图", "色图", "蛇图", "色色", "涩涩", "瑟图", "瑟瑟"], rule=Limit(60).limit,
                  priority=1, block=True)


@setu.handle()
async def __setu():
    msg = MessageChain(MessageSegment.image(
        url="https://api.sirin.top/release/PIXIV/random/thumbnails"))
    await setu.finish(msg)
