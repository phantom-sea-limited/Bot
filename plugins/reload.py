from nonebot_plugin_apscheduler import scheduler
from nonebot import require
from nonebot.log import logger
from .__reboot.rebot import Reloader
from nonebot import on_keyword
from Lib.Bot import BOT

require("nonebot_plugin_apscheduler")
reload = on_keyword(["Reload"], priority=1, block=True)


@reload.handle()
@scheduler.scheduled_job("cron", day="*/1", id="reload")
async def _reload():
    logger.info("Reloading!")
    b = BOT()
    b.reset()
    r = b.verify()
    b.bind(r["session"])
    Reloader.reload(5)
    # nonebot.run(app="__mp_main__:app")
