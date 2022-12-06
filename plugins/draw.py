from nonebot.adapters.mirai2.message import MessageChain, MessageSegment
from nonebot.adapters.mirai2.event import MessageEvent
from nonebot import on_keyword
import random

ability = on_keyword(["超能力"], priority=1, block=True)


@ability.handle()
async def __ability(event: MessageEvent):
    cnl = {
        "随机能力": ["与死者对话", "范围2km的自爆", "预知未来", "不用喝水吃饭也不会死", "玩任何游戏都能赢", "拥有狙击镜级别的视力", "可以治愈任何疾病", "可以睁着眼睛睡觉", "可以暂停时间", "可以复制任何物品", "可以自由控制自己的梦境", "可以飞行", "可以在现实生活中存读档", "双眼可以发射死亡辐射", "坐公交车可以看到哪些人下一站下车", "可以瞬间移动", "下雨的时候就算不撑伞也不会被雨淋到", "可以改变自己的外貌", "可以隐身", "可以瞬间给自己的手机充满电", "能够分身", "瞬间让自己睡着", "可以进行时间旅行", "永远都不会死", "每天可以召唤一桶泡面", "免疫所有疾病", "不需要睡觉", "永远不需要上厕所", "可以让银行卡里的钱翻倍", "精通任何一门外语", "站着拉屎", "可以在现实生活撤回上一步", "变得更好看", "反转性别", "喝酒不会醉", "可以变身成任何物体", "可以改变任何物体的颜色", "变身成为美少女", "成为偶像", "永远不会变老", "完全没有存在感", "复制其他人的超能力", "在脑中播放自己的网易云歌单", "不会感觉痛", "吸收别人的寿命", "不需要闹钟也能准时醒", "身体的任意部位可以发光", "百分百被空手夺白刃", "不用眨眼睛", "吃东西不会变胖", "可以在水里呼吸", "知道别人什么时候会死", "可以变出新的作业", "打喷嚏的时候能够睁开眼睛", "不会遇到其他超能力者", "无论身体多么虚弱都能发出临死的惨叫", "百分百遗言会说到一半咽气", "把别人的名字变成李狗蛋", "随时随地知道现在是什么时间", "让全世界的人随时随地都知道你在干什么", "让别人觉得自己没有超能力", "一生一次无视距离的瞬间移动", "扔骰子能骰出最大的结果", "魔女化", "抽卡必出金", "可以连续爆肝一星期", "让世界感受痛苦", "不用充电器可以给手机充电", "不死之身", "脑中的想法有几率成真的能力", "回到一分钟前", "桃花运旺盛", "身上永远不会脏", "可以将相同物品叠加", "透视", "变成女孩子", "抗打", "画风突变（当情绪大幅波动时，视野中的事物形态会发生改变，目击者的认知会发生偏移）", "灵媒", "获得无敌的力量", "使承诺必定达成的能力", "驱逐外力的能力", "可以分担他人的痛苦", "暂停时间的能力", "『归一之序』吃任何东西都不会掉渣", "『蠕行暗影』可以让你的鼻毛长在身上的任何地方", "『花开不败』你可以使任意一棵石楠的花期延长半年", "『颠倒的迈克尔』可以离地一毫米浮空十五秒并趁此表演无摩擦太空步", "『灵能之漩涡』当你躺着转椅上时，椅子会随着你的意念旋转起来！", " 『麻木的上校』你可以让你吃到的任何东西变成炸鸡口味", "『吐兰』你的舌头拥有智能，且比你本人更聪明，打开手机放在枕头边然后睡上一觉，你的舌头会码出一本《舌经》", "『消失的神灵』传教人士将永远不会出现在你的生活中", "『绿色人影』在脑海里回想起一个人，这个人会在第二天穿成一身亮绿色", "『不可名状的考试』英语完形填空题和选项必在同一面。", "『自知之明』知道自己有知道自己有超能力的超能力", "『赤蛮奇的注视』让头飞出去程度的能力", "『超能力者』操纵超能力程度的能力"],
        "随机代价": ["需要支付100000元", "即刻去世", "必须全程保持果体", "自己的寿命会减半", "身高减少20cm", "双目失明", "被全国通缉", "永远也找不到女朋友", "少一个肾", "什么事情都不会发生", "体重增加30kg", "自己会得癌症", "考试永远不及格", "失去生育能力", "以后再也没有办法上网", "再也不能啪啪啪了", "全世界所有人都会得到相同的能力", "自己会变丑", "智商-20", "性取向会反转", "只能在没有人的时候使用", "每天早上都会宿醉", "会永远拉稀", "每天都会失眠", "会导致世界末日", "性别会反转", "手机的电量会变成1%", "无法使用手机", "头发会变少", "随机丢失一段记忆", "忘掉自己的密码", "死后才能发动", "必须穿上女装", "死亡", "秃顶", "肾虚", "没有女朋友", "每天出门都会遭遇一次被足以杀死人类的意外", "不幸的想法必定成真", "回到一分钟前", "兴奋的时候强制冷静", "没有眉毛", "处于黑暗中会受到怪物攻击", "会不自禁的把内心所想说出来", "对病娇有致命吸引力", "挨打", "没有朋友", "生出奇怪的子嗣", "用久了就会逐渐女性化", "每次使用能力会永久失去1%头发", "身高固定为一米五", "随机失去部分肢体", "『本能抑制』拆除你所在城市里所有华莱士的厕所", "『恶意满盈』自动成为小孩讨厌的对象", " 『程序化休眠』在你睡着后，你只能也只会在八小时后醒来", "『爱丽丝之殇』你发出所有声音降低12分贝", "『虔诚的喉舌』无法再说出违心的话语", "『欲望死徒的救赎』觉醒一个你原本无法接受的xp", "『缪斯的魂灵』你的音乐审美变为广场舞大妈水平", "『禁电屏蔽』任何电子设备会在你附近5m内直接报废"],
        "超能力": ["\n你的超能力是【{%随机能力}】，发动能力的代价是【{%随机代价}】。"]
    }
    try:
        name = event.sender.name
    except Exception:
        name = event.sender.nickname
    msg = f'''{name}的超能力是{random.choice(cnl["随机能力"])},发动能力的代价是{random.choice(cnl["随机代价"])}'''
    await ability.finish(msg)
