import asyncio
from Instance import BOTInstanceInstance


async def recall(messageId, event, wait=5):
    try:
        target = event.sender.id
    except:
        target = event.sender.group.id
    await asyncio.sleep(wait)
    M = {
        "target": target,
        "messageId": messageId
    }
    await BOTInstanceInstance.sendMessage(M, "recall")
