from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot import on_keyword
from nonebot.matcher import Matcher
from plugins.__Limit import Limit
from dataclasses import dataclass
from nonebot.params import Depends
from .pixiv import Pixiv


@dataclass
class Key:
    key: list
    reply: MessageChain = False
    function: callable = False
    block: bool = True
    Limit: bool = False
    Depend: bool = False
    priority: int = 3


Keys = [
    Key(["???", "？？？"], MessageChain(MessageSegment.image(
        path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/chat/question.png"))),
    Key(["刑啊", "枪毙", "枪决", "击毙"], MessageChain(MessageSegment.image(
        path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/chat/kill.png"))),
    Key(["涩图", "色图", "蛇图", "色色", "涩涩", "瑟图", "瑟瑟"], function=Pixiv.random,
        Limit=Limit(60).limit, Depend=Limit(60).set),
    Key(["你好笨"], "不要打破第四面墙，你这小聪明鬼"),
    Key(["不想去"], "我们只是尘埃虫豸之辈而已"),
    Key(["不行"], "不，我们不会抛弃我们的人们!"),
    Key(["随便"], "让那个棺材继续它的旅途吧"),
    Key(["你去忙吧"], "我们只要你们的船就够了"),
    Key(["我不会"], "我们的预测模型显示你的未来如同一台面包机一样光明，给我砸了!"),
    Key(["你好烦"], "能不能麻烦你停止那个烦人的尖叫呢"),
    Key(["要你管"], "我从未想过自己会如此热爱他们的文化,我再也不会参加这次的破坏行动"),
    Key(["滚"], "我一直不明白你们是如何飞出母星的"),
    Key(["帮我个忙"], "让我入伙吧。不，不，我是说真的!我觉得我们会很合得来"),
    Key(["你陪我"], "过去与未来相互交织，唯有爱是永恒之物"),
    Key(["气死我了"], "我们将其称为高效")
]


def Handle():
    def run(k: Key):
        async def _main():
            if k.reply != False:
                return k.reply
            else:
                return await k.function()

        async def _handle(matcher: Matcher, d=Depends(k.Depend)):
            await matcher.finish(await _main())

        async def _handle2(matcher: Matcher):
            await matcher.finish(await _main())

        if k.Depend != False:
            return _handle
        else:
            return _handle2

    for i in Keys:
        if i.Limit != False:
            on_keyword(i.key, rule=i.Limit, block=i.block,
                       priority=i.priority).append_handler(run(i))
        else:
            on_keyword(i.key, block=i.block,
                       priority=i.priority).append_handler(run(i))


Handle()
