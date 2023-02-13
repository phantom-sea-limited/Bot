import os
import json
import random
import base64
import subprocess
from websockets.legacy.client import Connect
from nonebot.log import logger as LOG
from utils.Async import run_blocking_func
from Lib.log import Log
l = Log("WSClient")


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


class huggingfaceWss():
    API = "wss://*******.hf.space/queue/join"
    session_hash = generate_random_str(11)

    def __init__(self, FFMPEG=False, temp_path=os.path.join(".log", "audio")) -> None:
        if os.path.exists(temp_path) != True:
            os.mkdir(temp_path)
        self.path = temp_path
        if FFMPEG == False:
            self.FFMPEG = os.path.join(".log", "ffmpeg.exe")
        else:
            self.FFMPEG = FFMPEG

    def get_post(self, word):
        "输入格式化"
        return json.dumps({"fn_index": 0, "data": [word],
                           "session_hash": self.session_hash})

    async def input(self, word):
        ws = await Connect(self.API, logger=l, extra_headers={})
        l.info(f"[Start][INFO]\t{self.API}")
        while ws.open:
            r = await ws.recv()
            l.info(f"[Recv][INFO]\t{r}")
            r = json.loads(r)
            if r["msg"] == "send_hash":
                await ws.send(json.dumps(
                    {"session_hash": self.session_hash, "fn_index": 0}
                ))
            elif r["msg"] == "send_data":
                await ws.send(self.get_post(word))
            elif r["msg"] == "process_completed":
                await ws.close()
                if r["success"]:
                    return self.save(word, r['output']['data'])
                else:
                    return {"error": f"未知错误，API返回结果为{str(r['output'])}"}

    def save(self, word, data):
        "保存API获取的base64到文件,不同API设计不同，请注意重构"
        data = data[0]
        base = data.split(",")[1]
        Suffix = data.split(";")[0].split("/")[1]
        PATH = os.path.join(self.path, f"{word}.{Suffix}")
        with open(PATH, "wb") as f:
            f.write(base64.b64decode(base))
        return {"error": False, "PATH": PATH}

    def transform(self, PATH):
        OUT = f"{os.path.splitext(PATH)[0]}.amr"  # 我为什么当初要这么写呢？不知道
        cmd = f"{self.FFMPEG} -i {PATH} -ab 320k -ac 1 -ar 8000 {OUT} -y"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''):
            LOG.info(line.strip().decode('gbk'))
        if os.path.exists(OUT) != True:
            return {"error": "文件转换失败"}
        return {"error": False, "PATH": OUT}

    def base64(self, PATH):
        with open(PATH, "rb") as f:
            b = f.read()
        return str(base64.b64encode(b), encoding="utf-8")

    async def run(self, word):
        try:
            r = await self.input(word)
            if r["error"]:
                return {"error": "API ERROR:\n" + r["error"]}
            r = await run_blocking_func(self.transform, r["PATH"])
            # r = self.transform(r["PATH"])
            if r["error"]:
                return {"error": "SERVER ERROR:\n" + r["error"]}
            return {"error": False, "BASE64": self.base64(r["PATH"])}
        except Exception as e:
            errname = str(type(e)).split("'")[1]
            return {"error": f"{errname}\n{str(e.args())}"}


class AmadeusWss(huggingfaceWss):
    '''https://huggingface.co/mio/amadeus'''
    API = "wss://rcrwrate-mio-amadeus.hf.space/queue/join"


class BA_base(huggingfaceWss):
    '''https://huggingface.co/spaces/sayashi/vits-models'''
    API = "wss://sayashi-vits-models.hf.space/queue/join"
    fn_index = 0

    def get_post(self, word):
        return json.dumps({"fn_index": self.fn_index, "data": [word, "日语",
                          0.6, 0.668, 1], "session_hash": self.session_hash})

    def save(self, word, data):
        data = data[1]
        base = data.split(",")[1]
        Suffix = data.split(";")[0].split("/")[1]
        PATH = os.path.join(self.path, f"{word}.{Suffix}")
        with open(PATH, "wb") as f:
            f.write(base64.b64decode(base))
        return {"error": False, "PATH": PATH}


class Sorasaki_Hina(BA_base):
    "空崎日奈"
    fn_index = 51


class BA_Chinese_base(BA_base):

    def get_post(self, word):
        return json.dumps({"fn_index": self.fn_index, "data": [word, "中文",
                          0.6, 0.668, 1], "session_hash": self.session_hash})


class KeQing(BA_Chinese_base):
    "刻晴"
    fn_index = 87
