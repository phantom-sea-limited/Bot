from dataclasses import dataclass
from .amadeus import *
from Lib.Network import Network
from Lib.Translate import Bing
from plugins.__Limit import Limit
from nonebot import get_driver, on_startswith
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.adapters.mirai2.event import GroupMessage

s = Network({})


@dataclass
class Audio:
    keywords: list
    handle: huggingface


voice = (
    Audio(["Amadeus", "红莉栖", "助手"], Amadeus(s=s)),
    Audio(["saber", "阿尔托莉雅", "王"], Artoria(s=s)),
)


def handles():
    def run(a: Audio):
        async def _de(matcher: Matcher, event: GroupMessage, d=Depends(Limit(120).set)):
            text = event.get_plaintext()
            for i in a.keywords:
                text = text.replace(i, "")
            text = Bing(text, "ja", s).text
            A = a.handle
            driver = get_driver()
            A.FFMPEG = getattr(driver.config, "ffmpeg", A.FFMPEG)
            fin = A.run(text)
            logger.debug(fin)
            if fin["error"]:
                await matcher.finish(fin["error"])
            else:
                from Lib.Bot import BOT
                from Lib.Message import Message
                m = Message(event.sender.group.id)
                m.voice(base64=fin["BASE64"])
                r = BOT(s=s).sendMessage(m.get_message(), "sendGroupMessage")
                logger.info(r)
        return _de

    for i in voice:
        on_startswith(
            i.keywords, priority=1, rule=Limit(120).limit, block=True
        ).append_handler(run(i))


handles()
