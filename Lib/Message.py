class Message():
    def __init__(self, target: int, quote: int = 0) -> None:
        self.fin = {
            "target": int(target)
        }
        self.messageChain = []
        self.forward_init = False
        if quote != 0:
            self.fin["quote"] = int(quote)

    def input(self, messageChain):
        if isinstance(messageChain, str):
            self.plain(messageChain)
        elif isinstance(messageChain, MesssagePart):
            self.messageChain = messageChain.messageChain
        elif isinstance(messageChain, list):
            self.messageChain = messageChain
        else:
            raise ValueError(
                f"Type {type(messageChain).__name__} is not supported")

    def plain(self, text: str):
        self.messageChain.append({"type": "Plain", "text": text})

    def image(self, url: str):
        self.messageChain.append({"type": "Image", "url": url})

    def FlashImage(self, url: str):
        self.messageChain.append({"type": "FlashImage", "url": url})

    def at(self, id: int):
        self.messageChain.append({"type": "At", "target": int(id)})

    def voice(self, url=None, base64=None):
        self.messageChain.append(
            {"type": "Voice", "base64": base64, "url": url})

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


class MesssagePart:
    messageChain = []

    def __init__(self, messageChain=[]) -> None:
        self.messageChain = messageChain

    def __str__(self) -> str:
        return str(self.messageChain)

    def __getitem__(self, __item: str):
        return self.messageChain[__item]

    @classmethod
    def plain(cls, text: str):
        return cls([{"type": "Plain", "text": text}])

    @classmethod
    def image(cls, url: str):
        return cls([{"type": "Image", "url": url}])

    @classmethod
    def FlashImage(cls, url: str):
        return cls([{"type": "FlashImage", "url": url}])

    @classmethod
    def at(cls, id: int):
        return cls([{"type": "At", "target": int(id)}])

    @classmethod
    def voice(cls, url=None, base64=None):
        return cls([{"type": "Voice", "base64": base64, "url": url}])

    @classmethod
    def music(cls, kind: str = "NeteaseCloudMusic", title: str = "", summary: str = "幻海实验室", jumpUrl: str = "", pictureUrl: str = "https://d.sirin.top/tmp_crop_decode.jpg", musicUrl: str = "https://api.phantom-sea-limited.ltd/music.mp3", brief: str = ""):
        return cls([{
            "type": "MusicShare",
            "kind": kind,
            "title": title,
            "summary": summary,
            "jumpUrl": jumpUrl,
            "pictureUrl": pictureUrl,
            "musicUrl": musicUrl,
            "brief": brief
        }])

    @classmethod
    def Forward(cls, self, messageId: int = 0, senderId: int = 0, senderName: str = ""):
        forward = {"type": "Forward", "nodeList": []}
        if messageId != 0:
            forward["nodeList"].append({"messageId": messageId})
        if senderId != 0 and senderName != "":
            forward["nodeList"].append({
                "senderId": int(senderId),
                "senderName": senderName,
                "messageChain": self.messageChain
            })
        return cls([forward])

    def __add__(self, other):
        return MesssagePart(self.messageChain + other.messageChain)
