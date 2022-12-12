# -*- coding: UTF-8 -*-

# import logging
import json
from .AsyncNetwork import Network as requests
# LOG = logging.getLogger("BOT")
# LOG.setLevel(logging.INFO)
# T = logging.StreamHandler()
# LOG.addHandler(T)

BASE = "http://1.117.87.219:20000/"


def get_qs(qs: json, key: str):
    try:
        id = qs[key]
    except KeyError as err:
        return ""
    else:
        return id


class BOT():
    '''https://docs.mirai.mamoe.net/mirai-api-http/api/API.html'''

    def __init__(self, s=requests({})) -> None:
        self.session = s

    async def verify(self, verifyKey="1234567890"):
        data = {
            "verifyKey": verifyKey
        }
        r = await self.session.post(BASE + "verify", json=data)
        # LOG.info("POST:\t" + r.url + "\nDATA:\t" + str(data) + "\n\t" + r.text)
        return await r.json()

    async def bind(self, sessionKey="SINGLE_SESSION", qq=179334874):
        data = {
            "sessionKey": sessionKey,
            "qq": qq
        }
        r = await self.session.post(BASE + "bind", json=data)
        # LOG.info("POST:\t" + r.url + "\nDATA:\t" + str(data) + "\n\t" + r.text)
        return await r.json()

    async def info(self, sessionKey="SINGLE_SESSION"):
        r = await self.session.get(BASE + f"sessionInfo?sessionKey={sessionKey}")
        return self.check_and_reload(await r.json())

    async def peekLatestMessage(self, count: int = 10):
        url = "peekLatestMessage?count={}".format(str(count))
        r = await self.session.get(BASE + url)
        # LOG.info("GET:\t" + r.url + "\n\t" + r.text)
        return self.check_and_reload(await r.json())

    async def get_mess_by_id(self, messageId, target):
        url = f"messageFromId?messageId={messageId}&target={target}"
        r = await self.session.get(BASE + url)
        # LOG.info("GET:\t" + r.url + "\n\t" + r.text)
        return self.check_and_reload(await r.json())

    @staticmethod
    def Filtering_message(message: json, key: str):
        '''
        根据消息类别过滤消息
        key: FlashImage(闪照)/Image(图片)/Plain(文本)/At(@)/Quote(回复)/Forward(转发)
        '''
        fin = []
        for i in message["data"]:
            if i["type"] in ["FriendMessage", "GroupMessage"]:
                for j in i["messageChain"]:
                    if j["type"] == key:
                        fin.append(i)
                        break
        if len(fin) == 0:
            return {"err": "没找到对应的消息，或许是消息过于久远了", "data": []}
        else:
            return {"err": False, "data": fin}

    @staticmethod
    def Filtering_Plain(message: json, key: str):
        '''
        根据消息内文本过滤消息
        '''
        tmp = BOT.Filtering_message(message, "Plain")
        if len(tmp["data"]) == 0:
            return {"err": "没找到对应的消息，或许是消息过于久远了", "data": []}
        else:
            fin = []
            for i in tmp["data"]:
                for j in i["messageChain"]:
                    text = get_qs(j, "text")
                    if key in text:
                        fin.append(i)
                        break
            if len(fin) == 0:
                return {"err": "没找到对应的消息，或许是消息过于久远了", "data": []}
            return {"err": False, "data": fin}

    @staticmethod
    def Filtering_Group(message: json, id: int):
        "根据群ID筛选群会话"
        fin = []
        for i in message["data"]:
            if i["type"] == "GroupMessage":
                if i["sender"]["group"]["id"] == id:
                    fin.append(i)
        if len(fin) == 0:
            return {"err": "没找到对应的消息，或许是消息过于久远了", "data": []}
        else:
            return {"err": False, "data": fin}

    @staticmethod
    def Filtering_User(message: json, id: int):
        "根据用户ID筛选用户会话"
        fin = []
        for i in message["data"]:
            if i["type"] == "FriendMessage":
                if i["sender"]["id"] == id:
                    fin.append(i)
        if len(fin) == 0:
            return {"err": "没找到对应的消息，或许是消息过于久远了", "data": []}
        else:
            return {"err": False, "data": fin}

    @staticmethod
    def Filtering_messageChain(message: list, type: str):
        "筛选一个消息中的对应模块: FlashImage(闪照)/Image(图片)/Plain(文本)/At(@)/Quote(回复)/Forward(转发)"
        for i in message:
            if i["type"] == type:
                return {"err": False, "data": i}
        return {"err": "Filtering_messageChain无结果"}

    async def sendMessage(self, data: json, type="sendGroupMessage"):
        '''
        type: sendGroupMessage(群消息)/sendFriendMessage(好友消息)/recall(撤回)/sendNudge(戳一戳)
        '''
        r = await self.session.post(BASE+type, json=data)
        # LOG.info("POST:\t" + r.url + "\nDATA:\t" + str(data) + "\n\t" + r.text)
        self.check(await r.json())
        return await r.json()

    async def reset(self, sessionKey="SINGLE_SESSION"):
        data = {
            "sessionKey": sessionKey,
            "qq": 179334874
        }
        r = await self.session.post(BASE + "release", json=data)
        # LOG.info("POST:\t" + r.url + "\nDATA:\t" + str(data) + "\n\t" + r.text)
        return await r.json()

    def check(self, r):
        if r["code"] != 0:
            msg = {'target': 1019241536, 'messageChain': [
                {'type': 'Plain', 'text': f'消息发送异常{str(r)}'}]}
            self.sendMessage(msg, "sendFriendMessage")

    async def check_and_reload(self, r: dict):
        if r["code"] == 500:
            # self.reset()
            # self.bind(self.verify()["session"]) # SINGLE_SESSION MODE NOT NEED bind() SINGLE_SESSION模式无需bind()
            self.verify()
            return {"code": r["code"], "msg": r["msg"], "data": []}
        return r


if __name__ == "__main__":
    bot = BOT()
    r = bot.verify()
    bot.bind(r["session"])
