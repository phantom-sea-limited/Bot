from nonebot.matcher import Matcher
from nonebot.adapters.mirai2.event import GroupMessage
from Instance import BOTInstanceInstance as Bot


class BAN():

    @staticmethod
    async def check(matcher: Matcher, event: GroupMessage):
        "验证是否触发ban"
        return False

    @staticmethod
    async def function(matcher: Matcher, event: GroupMessage):
        "ban的具体操作"
        return None


class img():

    @staticmethod
    async def check(matcher: Matcher, event: GroupMessage):
        "验证是否触发ban"
        img_ban_list = ['{3B68602A-7396-A596-9DBE-1EF4B3DD8818}.gif', '{CCD74CD4-2685-A6F7-782D-1D6725E0EFC6}.jpg','{7056065C-BEDB-7ABF-B2AD-5E9BD0A99947}.gif']
        fin = Bot.Filtering_messageChain(
            event.normalize_dict()['message_chain'], "Image")
        if fin["err"] == False:
            if fin["data"]["data"]["imageId"] in img_ban_list:
                return True
        return False

    @staticmethod
    async def function(matcher: Matcher, event: GroupMessage):
        "ban的具体操作"
        print("OK")
        M = {
            "target": event.sender.group.id,
            "messageId": event.source.id
        }
        await Bot.sendMessage(M, "recall")
        return None
