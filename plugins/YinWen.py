from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot import on_type
import random
from Lib.Bot import BOT
# 淫纹刻印时间到


yw = on_type(GroupMessage, priority=10)


@yw.handle()
def __yw(event: GroupMessage):
    if random.randint(0, 1000) <= 100:  # 激活判定
        scale = random.randint(0, 1000)  # 成功检定
        if scale >= 900 or scale <= 100:  # 邪神手滑了
            b = BOT()
            r = b.peekLatestMessage(10)
            r = b.Filtering_Group(r, event.sender.id)
        else:  # 中嘞,哥
            pass
