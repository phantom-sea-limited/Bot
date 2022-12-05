from nonebot_plugin_apscheduler import scheduler
from nonebot import require
from Lib.Bot import BOT
from Lib.Message import Message
from Lib.Network import Network
from nonebot.log import logger
import time
require("nonebot_plugin_apscheduler")


@scheduler.scheduled_job("cron", hour="*/1", id="xxx", args=[1], kwargs={"arg2": 2})
async def run_every_1_hour(arg1, arg2):
    t = time.strftime("%H", time.localtime())
    if int(t) > 7:
        n = Network({})
        r = n.get(
            f"https://api.sirin.top/release/PIXIV/ranking?mode=daily&top={int(t)-7}").json()
        m = Message(960290056)
        m.plain(f'''PID {r["body"]["id"]}\n''')
        m.image(r["body"]["urls"]["original"].replace(
            "i.pixiv.re", "piv.deception.world"))
        r = BOT().sendMessage(m.get_message(), "sendGroupMessage")
        logger.info(str(r))
