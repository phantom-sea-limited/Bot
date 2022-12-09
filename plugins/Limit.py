from nonebot.adapters.mirai2.event import MessageEvent
from Lib.ini import CONF

def limit(event: MessageEvent):
    event.get_user_id()
