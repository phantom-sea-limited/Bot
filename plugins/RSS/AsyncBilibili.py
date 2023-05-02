import json
from Code.AsyncBilibili import Bilibili
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
        while Did == "":
            tmp = data['data']['items'].pop(0)
            if "module_tag" in tmp['modules'].keys():
                if tmp['modules']['module_tag']['text'] != '置顶':
                    Did = tmp['id_str']
            else:
                Did = tmp['id_str']
        return {"UID": UID, "Did": Did, "LS": await self.IsLiveNow(UID), "body": tmp}

    async def analysis(self, UID):
        old = self.cache(UID)
        new = await self.fetch(UID)
        if old == False:  # 初始化订阅
            self.cache(UID, new)
            return False
        else:
            self.cache(UID, new)
            if new["LS"] == True and old["LS"] == False:
                new["LS"] = True
            else:
                new["LS"] = False
            if new["Did"] == old["Did"]:
                new["body"] = False
            return new

    async def transform(self, data, msg=""):
        if data["body"] != False:
            return self.getDynamicInfo(data["body"])
        if data["LS"] == True:
            info = await self.spaceInfo(data["UID"])
            return MesssagePart.plain(
                info["data"]["name"] + "正在直播:\n" + info['data']['live_room']['title'] +
                "\n" + info['data']['live_room']['url']
            ) + \
                MesssagePart.image(info['data']['live_room']['cover'])
        return False
