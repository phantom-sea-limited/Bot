import random
import time
from nonebot import on_type
from nonebot.adapters.mirai2.event import GroupMessage
from Instance import BOTInstanceInstance as b
from Lib.ini import CONF
from .__face import face
# 淫纹刻印时间到


yw = on_type(GroupMessage, priority=10)
c = CONF("YinWen")

@yw.handle()
async def __yw(event: GroupMessage):
    ywmsg = {
        "邪神": [
            "阿布霍斯",
            "阿特拉克·纳克亚",
            f"阿萨托斯，顺带着其他{random.randint(1, 9)}名邪神",
            "阿萨托斯",
            "芭丝特",
            "昌格纳·方庚",
            "克图格亚",
            "克苏鲁",
            "赛伊格亚",
            "道罗斯",
            "埃霍特",
            "加塔诺托亚",
            "格拉基",
            "哈斯塔",
            "伊塔库亚",
            "黄衣之王",
            "奈亚拉托提普",
            "尼约格萨",
            "兰-提格斯",
            "莎布-尼古拉斯",
            "修德梅尔",
            "撒托古亚",
            "图尔兹查",
            "乌波·萨斯拉",
            "伊波·兹特尔",
            "伊格",
            "犹格·索托斯",
            "佐斯·奥摩格"
        ],
        "手滑": [
            "{god}注视着{name},祂感到非常好奇,祂决定赐予什么,但是祂手滑了,或许是故意的,{other}的身上默默浮现出了一个淫纹\n{yw}",
            "{name}的发言吸引到了{god}的注视,很神秘,祂又撇了一眼{other},{other}的身上默默浮现出了一个淫纹\n{yw}",
            "{god}很无聊,祂随意扔了点东西,{name}很幸运,或许是注定,小礼物砸到了{other}\n{yw}",
            "{name}不知道干了啥,突然收到了一份充斥着无尽憎恨的礼物,但是快递送错了,收货人变成了{other}\n{yw}"
        ],
        "情景": [
            "{god}注视着{name},祂感到非常好奇,祂决定赐予什么\n{yw}",
            "{name}的发言吸引到了{god}的注视,这是一位神的注视,{name}的身上默默浮现出了一个淫纹\n{yw}",
            "{god}很无聊,祂随意扔了点东西,当然,{name}是礼物的收件人,这一切都是命中注定\n{yw}",
            "{god}赐予了{name}一件恐龙玩偶睡衣,但是触手衣装,{name}感觉腹部热热的,酱酱,是发光淫纹\n{yw}",
            "{name}吵醒了{god},祂抢了触手酱的玩具,一个针筒,很快{name}醒来发现自己变成了小萝莉,还有淫纹\n{yw}",
            "{name}不知道干了啥,突然收到了一份充斥着无尽憎恨的礼物\n{yw}",
            "{name}身上有非常神奇的吸引力,以至于吸引到了{god},不过,在这之后似乎被当做“朋友”消耗掉了",
            "过度的欲望使人疯狂,{god}在{name}的脑中轻轻呼唤,████"
        ],
        "淫纹": [
            "奴隶\n违抗命令时会感到痛苦与难受",
            "容器\n时常感到疲倦与虚弱\n除非体内有新鲜的精液",
            "吸引\n当附近有男性时。如果对方超过1米就会感到难受",
            "子宫高潮\n只有精液穿过子宫口时才能高潮，子宫里没有精液就会不断发情",
            "数据统计\n做爱与高潮的数据将显示在身体上",
            "娇艳\n身体会随着欲望的增加而变化\n使胸臀嘴变得愈加丰满",
            "自卑\n当与男性交合时会贬低自身\n甚至对对方产生崇拜之情",
            "凄凉\n失落 害怕 恐惧会产生最强烈的情欲",
            "改写\n可令其改写自身的性格与思维等方面，睡过一觉之后就会产生变化，暂时性效果。",
            "发光\n淫纹会发光，可穿透20CM厚的布料或3CM厚的物体，使淫纹无法隐藏",
            "命令\n被下命令时必须服从。只能同时下一个命令。未指定时间命令持续一小时。",
            "生殖高潮\n被中出时会变为拟似怀孕的状态，并在两小时后会产下胚胎大小的蛋。出产时会获得与痛苦同等程度的高潮。蛋被打破会使自身在一小时内变温顺。",
            "兽化\n性奋时会发出与自身最相似的动物般的叫声。在与男性亲热时则会发出他认为最贴切的动物叫声。",
            "汲取\n如果男性在触摸自身的同时高潮，会让对方整天感到精力充沛，并使自身萎靡不振。效果可累加。",
            "迎合\n可感觉到10米内的男性对自身的意淫，并产生让对方的幻想变为现实的冲动。",
            "魂锁\n无论是否合意，只要被男性亲吻就会无法入眠，直到被对方中出或者被要求离开为止。效果也会在三个晚上后消失",
            "毁灭\n如果在怀孕时被中出，胚胎将死亡并在十天内液化。在此期间内产生的高潮强烈程度与持续时间都是以往的三倍。可能会对此上瘾。",
            "解放\n无法在公共场合完全遮蔽自己的身体，只能穿着不会妨碍交合的衣物。款式可任意变化，通常包含使自己无法抗拒被侵犯的自我绑缚。",
            "被虐\n被男性虐待时会感到兴奋，并无可救药地爱上对方，并不会减少或转化痛苦",
            "精瘾\n下次尝到精液时会对其上瘾，二十四小时未摄入会出现严重戒断反应，精液也可以通过阴部或肛门摄入",
            "凝视\n每当被好色的目光注视时，体内会产生一种震动棒被打开的感觉，第一次持续一分钟，随后当天每次触发增加十秒",
            "触发\n刻上淫纹时，可使其对两个不同的短句产生反应，听到第一个短句时会变得更加好色，听到第二个短句时会变得更加服从",
            "深度专注\n可以细微的感受到性器内发生的一切，从阴唇到卵巢，脑海中可以显现出精液射入时的景象，受精会带来足以引起精神崩溃的高潮",
            "任务\n必须在二十四小时之内完成指定的任务，完成之前无法回家或睡觉，若未完成指定任务，则需要被陌生人爱抚五分钟，每周最多可以指定五个任务",
            "敏感\n原本性感带的敏感度增加三倍，且胸口往下直到大腿的部分都变得和原性感带一样敏感",
            "费洛蒙\n附近三十米内的男性都将被吸引并对其产生性趣，距离越近效果越强。",
            "心智融化\n每次高潮都将失去一部分记忆，每次高潮都将带来更加强烈的欲望。",
            "情欲\n欲望高涨到完全无法自己，毕生都将不断自慰，或是乞求男性与其不断交合中渡过。",
            "思维信息\n下流的想法会显示在皮肤上，使其成为行走的性爱广告牌。",
            "子宫高潮\n只有精液穿过子宫口时才会高潮，子宫里没有精液时就会不断发情。",
            "吸引\n当附近有男性时，如果距离超过一米就会感到难受",
            "盲从\n会相信男性说的任何话，信念因此受到影响，而改变的越大就会变得越温顺，变化的效果很慢，但效果永久",
            "泌乳\n胸部变大并且开始分泌乳汁，被榨的越多快感越强烈，可能会对此上瘾。",
            "受苦\n痛苦变为快感，温柔和友善变为恶心，强暴变为情欲，爱情则变为麻木",
            "未完待续",
            "未完待续",
            "未完待续"
        ],
    }
    # print(event.dict())
    if random.randint(0, 1000) <= 5:  # 激活判定
        t = time.strftime("%Y-%m-%d", time.localtime())
        if c.load(str(event.sender.id), "day")[0] != t:
            c.add(str(event.sender.id), "day", t)
            c.save()
            if random.randint(0, 1000) <= 100:  # 邪神手滑了
                r = await b.peekLatestMessage(10)
                try:
                    r = b.Filtering_Group(r, event.sender.group.id)
                    target = random.choice(r["data"])
                    if target["sender"]["id"] == event.sender.id:  # 手滑但没完全手滑
                        msg = random.choice(ywmsg["情景"]).format(
                            god=random.choice(ywmsg["邪神"]),
                            name=event.sender.name,
                            yw=random.choice(ywmsg["淫纹"]),
                        )
                        await yw.finish(msg, quote=event.dict()["source"]["id"])
                    else:
                        msg = random.choice(ywmsg["手滑"]).format(
                            god=random.choice(ywmsg["邪神"]),
                            name=event.sender.name,
                            yw=random.choice(ywmsg["淫纹"]),
                            other=target["sender"]["memberName"]
                        )
                        await yw.finish(msg, quote=event.dict()["source"]["id"])
                except Exception:
                    pass
            else:  # 中嘞,哥
                msg = random.choice(ywmsg["情景"]).format(
                    god=random.choice(ywmsg["邪神"]),
                    name=event.sender.name,
                    yw=random.choice(ywmsg["淫纹"]),
                )
                await yw.finish(msg, quote=event.dict()["source"]["id"])

    if random.randint(0, 1000) <= 20:  # 激活判定
        await yw.finish(random.choice(face))
