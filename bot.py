#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.mirai2 import Adapter as MIRAI2Adapter

# Custom your logger
#
from nonebot.log import logger, default_format
import os
logger.add(os.path.join(".log", "debug", "debug.log"),
           rotation="00:00",
           diagnose=False,
           level="DEBUG",
           format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(MIRAI2Adapter)


# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
# nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...
if __name__ == "__mp_main__":  # 仅在子进程运行的代码
    # Please DO NOT modify this file unless you know what you are doing!
    # As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
    # 加载插件
    nonebot.load_from_toml("pyproject.toml")


if __name__ == "__main__":
    nonebot.logger.warning(
        "Always use `nb run` to start the bot instead of manually running!")
    # nonebot.load_from_toml("pyproject.toml")
    nonebot.run(app="__mp_main__:app")
