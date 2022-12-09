from nonebot import on_startswith
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot.log import logger
from nonebot.params import Depends
from plugins.__Limit import Limit


__amadeus = on_startswith(["Amadeus", "红莉栖", "助手"],
                       rule=Limit(120).limit, priority=1)


@__amadeus.handle()
async def _amadeus(event: GroupMessage, d=Depends(Limit(120).set)):
    text = event.get_plaintext()
    for i in ["Amadeus", "红莉栖", "助手"]:
        text = text.replace(i, "")
    from Lib.Network import Network
    from Lib.Translate import Bing
    from .amadeus import Amadeus
    s = Network({"api-inference.huggingface.co": {"ip": "184.72.248.176"}})
    text = Bing(text, "ja", s).text
    fin = Amadeus(s=s).run(text)
    logger.debug(fin)
    if fin["error"]:
        await __amadeus.finish(fin["error"])
    else:
        from Lib.Bot import BOT
        from Lib.Message import Message
        m = Message(event.sender.group.id)
        m.voice(base64=fin["BASE64"])
        r = BOT(s=s).sendMessage(m.get_message(), "sendGroupMessage")
        logger.info(r)
