from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot.adapters.mirai2.event import GroupMessage
from nonebot import on_type
import random
# 淫纹刻印时间到


yw = on_type(GroupMessage, priority=10)


@yw.handle()
def __yw(event: GroupMessage):
    pass
