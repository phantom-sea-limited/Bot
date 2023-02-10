from dataclasses import dataclass
from typing import Union
from nonebot import get_driver, on_startswith
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.adapters.mirai2.event import GroupMessage
from Instance import NetworkInstance as s
from Instance import FFMPEG
from Lib.AsyncTranslate import Bing
from plugins.__Limit import Limit
from .amadeus import *
from .amadeusWss import *


@dataclass
class Audio:
    keywords: list
    handle: Union[huggingface, huggingfaceWss]
    translate: bool = True


voice = (
    Audio(["Amadeus", "红莉栖", "助手"], AmadeusWss(FFMPEG=FFMPEG)),
    Audio(["saber", "阿尔托莉雅", "王"], Artoria(s=s, FFMPEG=FFMPEG)),
    Audio(["空崎 ヒナ", "空崎日奈"], Sorasaki_Hina(FFMPEG=FFMPEG)),
)


def handles():
    def run(a: Audio):
        async def _de(matcher: Matcher, event: GroupMessage, d=Depends(Limit(120).set)):
            text = event.get_plaintext()
            for i in a.keywords:
                text = text.replace(i, "")
            if a.translate:
                try:
                    text = await Bing(s).run(text, "ja")
                except Exception:
                    matcher.finish("Translate ERROR:\n翻译API失效")
            # text = Bing(text, "ja").text
            A = a.handle
            driver = get_driver()
            A.FFMPEG = getattr(driver.config, "ffmpeg", A.FFMPEG)
            fin = await A.run(text)
            logger.debug(fin)
            if fin["error"]:
                await matcher.finish(fin["error"])
            else:
                from Instance import BOTInstanceInstance as BOT
                from Lib.Message import Message
                m = Message(event.sender.group.id)
                m.voice(base64=fin["BASE64"])
                r = await BOT.sendMessage(m.get_message(), "sendGroupMessage")
                logger.info(r)
        return _de

    for i in voice:
        on_startswith(
            i.keywords, priority=1, rule=Limit(120).limit, block=True
        ).append_handler(run(i))


handles()
