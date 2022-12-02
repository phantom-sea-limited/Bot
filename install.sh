python -m venv venv
source ./venv/bin/activate
pip install nonebot
pip install nonebot_adapter_mirai2
pip install requests
pip install nonebot_plugin_apscheduler
# pip install cn2an
# pip install aiohttp
# pip install cachetools
# pip install Pillow
pip install bs4
cd plugins/nonebot_plugin_gamedraw
poetry install
cd ../../
python bot.py