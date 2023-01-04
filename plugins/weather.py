from Lib.AsyncNetwork import Network
from urllib.parse import quote
import re
import json
from nonebot.adapters.mirai2.event import Event
from nonebot import on_keyword
from .__Limit import Limit
from nonebot.params import Depends


async def Weather(word, s=Network({})):
    r = await s.get(f"https://cn.bing.com/search?q={quote(word)}")
    r = await r.text()
    wea = re.findall(
        r'''if \(LGWeather\) { LGWeather.init\(([\s\S]+?),false,false\); };''', r)[0]
    wea = '{"L1":' + wea.replace("{0}", "0").replace("{1}", "1").replace(
        "],[", '],"L2":[').replace("],{", '],"L3":{') + "}"
    wea = json.loads(wea)
    wea["locate"] = re.findall(
        r'''<span class="wtr_foreGround">([\s\S]+?)</span>''', r)[0]
    return wea


weather = on_keyword(["天气", "tianqi"], priority=2,
                     rule=Limit(120).limit, block=True)


@weather.handle()
async def _(event: Event, d=Depends(Limit(120).set)):
    word = event.get_plaintext()
    try:
        r = await Weather(word)
        msg = r["locate"] + "\t" + r["L1"][0]["Title"] + "\n最高温" + \
            r["L1"][0]["High"] + "C°,最低温" + r["L1"][0]["Low"] + \
            "C°" + "\n风速" + r["L1"][0]["Wind"] + \
            "\n今日份的太阳将在" + r["L1"][0]["Sunset"] + "时落下"
    except Exception:
        msg = "没能找到这个地区的天气呢"
        import traceback
        print(traceback.format_exc())
    await weather.finish(msg)
