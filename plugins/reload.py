from nonebot import require
from nonebot.log import logger
from nonebot import on_keyword
from nonebot.permission import SUPERUSER
from nonebot_plugin_apscheduler import scheduler
from Instance import BOTInstanceInstance as BOT
from .__reboot.rebot import Reloader

require("nonebot_plugin_apscheduler")
reload = on_keyword(["Reload"], priority=1, block=True, permission=SUPERUSER)


@reload.handle()
@scheduler.scheduled_job("cron", day="*/1", id="reload")
async def _reload():
    logger.info("Reloading!")
    # b = BOT()
    # b.reset()
    # r = b.verify()
    # b.bind(r["session"])
    Reloader.reload(5)
    # nonebot.run(app="__mp_main__:app")


@scheduler.scheduled_job("cron", hour="*/4", id="reload_http")
async def _reload_http():
    logger.info("Reloading http!")
    await BOT.verify()
