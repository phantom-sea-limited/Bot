class Message():
    def __init__(self, target: int, quote: int = 0) -> None:
        self.fin = {
            "target": int(target)
        }
        self.messageChain = []
        self.forward_init = False
        if quote != 0:
            self.fin["quote"] = int(quote)

    def plain(self, text: str):
        self.messageChain.append({"type": "Plain", "text": text})

    def image(self, url: str):
        self.messageChain.append({"type": "Image", "url": url})

    def FlashImage(self, url: str):
        self.messageChain.append({"type": "FlashImage", "url": url})

    def at(self, id: int):
        self.messageChain.append({"type": "At", "target": int(id)})

    def music(self, kind: str = "NeteaseCloudMusic", title: str = "", summary: str = "幻海实验室", jumpUrl: str = "", pictureUrl: str = "https://d.sirin.top/tmp_crop_decode.jpg", musicUrl: str = "https://api.phantom-sea-limited.ltd/music.mp3", brief: str = ""):
        self.messageChain.append({
            "type": "MusicShare",
            "kind": kind,
            "title": title,
            "summary": summary,
            "jumpUrl": jumpUrl,
            "pictureUrl": pictureUrl,
            "musicUrl": musicUrl,
            "brief": brief
        })

    def Forward(self, messageId: int = 0, senderId: int = 0, senderName: str = ""):
        if self.forward_init == False:
            self.forward = {"type": "Forward", "nodeList": []}
            self.forward_init = True
        if messageId != 0:
            self.forward["nodeList"].append({"messageId": messageId})
        if senderId != 0 and senderName != "":
            self.forward["nodeList"].append({
                "senderId": int(senderId),
                "senderName": senderName,
                "messageChain": self.messageChain
            })
            self.messageChain = []
        pass

    def get_message(self):
        if self.forward_init != False:
            self.messageChain.append(self.forward)
            del self.forward
            self.forward_init = False
        self.fin["messageChain"] = self.messageChain
        self.messageChain = []
        return self.fin


if __name__ == "__main__":
    m = Message(960290056)
    m.plain("我是死猫~喵")
    m.Forward(senderId=2788781632, senderName="可爱的死猫")
    m.plain("主人~主人~~")
    m.image("https://ts1.cn.mm.bing.net/th?id=OIP-C.IISHfBHKDT6sE6mdOZz6OAAAAA&w=192&h=170&c=8&rs=1&qlt=90&o=6&dpr=1.25&pid=3.1&rm=2")
    m.Forward(senderId=2788781632, senderName="可爱的死猫")
    data = m.get_message()
    from Bot import BOT
    b = BOT()
    # b.sendMessage(data)
