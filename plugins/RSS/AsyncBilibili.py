import json
import time
from nonebot.log import logger
from Instance import BiliInstance as Bilibili
from Lib.Message import MesssagePart
from Lib.AsyncNetwork import Network
from .AsyncRss import RSS


class BiliRss(Bilibili, RSS):
    sec = "BiliBili"
    hour = "*"
    minute = "*/6"
    wait = 10

    def __init__(self, s=Network({}), c=...) -> None:
        RSS.__init__(self, n=s, c=c)
        Bilibili.__init__(self, s)

    @staticmethod
    def getDynamicInfo(single):
        pub_action = single['modules']['module_author']['pub_action']
        if pub_action == "":
            pub_action = "发表了动态"
            TYPE = None
        elif pub_action == "投稿了视频":
            TYPE = "Video"
        elif pub_action == "投稿了文章":
            TYPE = "Article"
        else:
            logger.error(f"BiliRSS TYPE NOT FOUND:\n\t{str(single)}")
            return False
        msg = MesssagePart.plain(
            single['modules']['module_author']['name'] + pub_action + "\n")
        if single['modules']['module_dynamic']['desc'] != None:
            msg += MesssagePart.plain(
                single['modules']['module_dynamic']['desc']['text'])
        if single['modules']['module_dynamic']['major'] != None:
            if TYPE == "Video":
                msg += MesssagePart.plain(
                    single['modules']['module_dynamic']['major']['archive']['desc']
                ) + \
                    MesssagePart.image(
                    single['modules']['module_dynamic']['major']['archive']['cover']
                ) + \
                    MesssagePart.plain(
                    "\nhttps:" + single['modules']['module_dynamic']['major']['archive']['jump_url'])
            elif TYPE == "Article":
                msg += MesssagePart.plain(
                    single['modules']['module_dynamic']['major']['opus']['title'] + "\n"
                ) + \
                    MesssagePart.plain(
                    single['modules']['module_dynamic']['major']['opus']['summary']['text']
                ) + MesssagePart.image(single['modules']['module_dynamic']['major']['opus']['pics'][0]['url']) + \
                    MesssagePart.plain(
                        "https:" + single['modules']['module_dynamic']['major']['opus']['jump_url'])
            else:
                for i in single['modules']['module_dynamic']['major']['draw']['items']:
                    msg += MesssagePart.image(i['src'])
        if TYPE == None:
            msg += MesssagePart.plain(
                "https://t.bilibili.com/" + single['id_str'])
        return msg

    def cache(self, uid, data: str = ""):
        if data == "":
            tmp = super().cache(str(uid), "")
            if tmp == False:
                return False
            else:
                return json.loads(tmp)
        return super().cache(str(uid), json.dumps(data))

    async def fetch(self, UID):
        data = await self.DynamicList(UID)
        Did = ""
        Live = False
        while Did == "":
            tmp = data['data']['items'].pop(0)
            if tmp["type"] == "DYNAMIC_TYPE_LIVE_RCMD":
                # 过滤直播动态,通过动态是否存在直播动态来判断直播,取代访问个人中心的方式(个人中心访问存在过多412和code-799)
                Live = True
            elif "module_tag" in tmp['modules'].keys():
                if tmp['modules']['module_tag']['text'] != '置顶':
                    Did = tmp['id_str']
            else:
                Did = tmp['id_str']
        return {"UID": UID, "Did": Did, "LS": Live, "body": tmp}

    async def analysis(self, UID):
        old = self.cache(UID)
        new = await self.fetch(UID)
        self.DataMap(UID, new["body"]['modules']['module_author']['name'])
        if old == False:  # 初始化订阅
            self.cache(UID, new)
            return False
        else:
            self.cache(UID, new)
            if new["LS"] == True and old["LS"] == False:
                new["LS"] = True
            elif new["LS"] == False and old["LS"] == True:
                new['LS'] = False
                new['body'] = False
                # 直播前后动态的最新DId会变动(划掉),这次更新已经剔除了直播动态的Did,但是留着也不影响
            else:
                new["LS"] = False
            if new["Did"] == old["Did"]:
                new["body"] = False
            return new

    async def transform(self, data, msg=""):
        if data["body"] != False:
            if time.time()-data["body"]["modules"]["module_author"]["pub_ts"] >= 3600:
                # 检查动态时间距今是否超过1小时，超过忽略
                return False
            else:
                return self.getDynamicInfo(data["body"])
        if data["LS"] == True:
            info = await self.spaceInfo(data["UID"])
            return MesssagePart.plain(
                info["data"]["name"] + "正在直播:\n" + info['data']['live_room']['title'] +
                "\n" + info['data']['live_room']['url']
            ) + \
                MesssagePart.image(info['data']['live_room']['cover'])
        return False

    async def TranslateID(self, ID):
        new = await self.fetch(ID)
        return new["body"]['modules']['module_author']['name']

    def start(self):
        return [self.InitMAP]
