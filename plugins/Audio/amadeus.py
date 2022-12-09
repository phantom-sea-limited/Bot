from Lib.Network import Network
import os
import subprocess


class LOG():
    def info(msg):
        print(msg)


class huggingface():
    API = "https://api-inference.huggingface.co/models/mio/amadeus"
    FFMPEG = ".log\\audio\\ffmpeg.exe"
    log = LOG()

    def __init__(self, temp_path=".log\\audio", s=Network(
            {"api-inference.huggingface.co": {"ip": "184.72.248.176"}})) -> None:
        if os.path.exists(temp_path) != True:
            os.mkdir(temp_path)
        self.path = temp_path
        self.s = s

    def input(self, word):
        data = {"inputs": word}
        r = self.s.post(self.API, json=data)
        try:
            return r.json()
        except Exception:
            Path = os.path.join(self.path, f"{word}.flac")
            with open(Path, "wb") as f:
                f.write(r.content)
            return {"error": False, "Path": Path}

    def transform(self, PATH):
        OUT = f"{PATH[:-4]}amr"
        cmd = f"{self.FFMPEG} -i {PATH} -ab 320k -ac 1 -ar 8000 {OUT} -y"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''):
            self.log.info(line.strip().decode('gbk'))
        if os.path.exists(OUT) != True:
            return {"error": "文件转换失败"}
        return {"error": False, "PATH": OUT}

    def run(self, word):
        r = self.input(word)
        if r["error"]:
            return {"error": "API ERROR:\n" + r["error"]}
        r = self.transform(r["Path"])
        if r["error"]:
            return {"error": "SERVER ERROR:\n" + r["error"]}
        return {"error": False, "PATH": r["PATH"]}


class Amadeus(huggingface):
    API = "https://api-inference.huggingface.co/models/mio/amadeus"
