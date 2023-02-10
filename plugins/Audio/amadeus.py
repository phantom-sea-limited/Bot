import os
import subprocess
import base64
from nonebot.log import logger as LOG
from Lib.AsyncNetwork import Network


class huggingface():
    API = "https://api-inference.huggingface.co/models/"

    def __init__(self, FFMPEG=False, temp_path=os.path.join(".log", "audio"), s=Network({})) -> None:
        if os.path.exists(temp_path) != True:
            os.mkdir(temp_path)
        self.path = temp_path
        self.s = s
        if FFMPEG == False:
            self.FFMPEG = os.path.join(".log", "ffmpeg.exe")
        else:
            self.FFMPEG = FFMPEG

    async def input(self, word):
        data = {"inputs": word}
        r = await self.s.post(self.API, json=data)
        try:
            return await r.json()
        except Exception:
            Path = os.path.join(self.path, f"{word}.flac")
            with open(Path, "wb") as f:
                f.write(await r.read())
            return {"error": False, "PATH": Path}

    def transform(self, PATH):
        OUT = f"{PATH[:-4]}amr"
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
        r = await self.input(word)
        if r["error"]:
            return {"error": "API ERROR:\n" + r["error"]}
        r = self.transform(r["PATH"])
        if r["error"]:
            return {"error": "SERVER ERROR:\n" + r["error"]}
        return {"error": False, "BASE64": self.base64(r["PATH"])}


class Amadeus(huggingface):
    '''https://huggingface.co/mio/amadeus'''
    API = "https://api-inference.huggingface.co/models/mio/amadeus"


class Artoria(huggingface):
    '''https://huggingface.co/mio/Artoria'''
    API = "https://api-inference.huggingface.co/models/mio/Artoria"
