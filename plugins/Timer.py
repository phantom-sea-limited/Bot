import time
import asyncio
from nonebot import require
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from Instance import BOTInstanceInstance as BOT
from Lib.Message import Message
from Instance import NetworkInstance as n


require("nonebot_plugin_apscheduler")


@scheduler.scheduled_job("cron", hour="*/1", id="xxx", args=[1], kwargs={"arg2": 2})
async def run_every_1_hour(arg1, arg2):
    await asyncio.sleep(5)
    t = time.strftime("%H", time.localtime())
    if int(t) > 7:
        r = await n.get(f"https://api.sirin.top/release/PIXIV/ranking?mode=daily&top={int(t)-7}")
        r = await r.json(content_type="text/json")
        m = Message(960290056)
        m.plain(f'''PID {r["body"]["id"]}\n''')
        m.image(r["body"]["urls"]["original"].replace(
            "i.pixiv.re", "piv.sirin.top"))
        r = await BOT.sendMessage(m.get_message(), "sendGroupMessage")
        logger.info(str(r))
