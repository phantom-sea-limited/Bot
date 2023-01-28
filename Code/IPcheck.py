import time
from Lib.Network import Network


class IPcheck():
    def __init__(self, ips, host) -> None:
        self.ips = ips
        self.host = host

    def run(self):
        result = {"ping": 1000}
        for ip in self.ips:
            tol = 0
            for i in range(1, 6):
                s = Network({self.host: {"ip": ip}})
                start = time.time()
                try:
                    r = s.get(url=f"https://{self.host}", allow_redirects=False, timeout=(5, 10))
                except Exception as err:
                    print(err.args)
                end = time.time()
                s.s.close()
                del s
                tol += end-start
                # time.sleep(1)
            tol = tol/5
            if tol <= result["ping"]:
                result["ip"] = ip
                result["ping"] = tol
            print(f"{ip}\t{r.status_code}\t\t{tol}\n")
        print(result)
        return result


if __name__ == "__main__":
    #     st = '''178.175.129.254
    # 178.175.128.252
    # 178.175.132.20
    # 178.175.128.254
    # 178.175.129.252
    # 178.175.132.22'''
    #     ips = st.split("\n")
    #     host = "EXHENTAI.ORG"
    #     r = IPcheck(ips,host).run()
    #     print(r)

    st = '''172.67.0.127
104.20.135.21
104.20.134.21'''
    ips = st.split("\n")
    ips = ["178.175.129.254", "178.175.132.20", "178.175.132.22",
           "178.175.128.252", "178.175.128.254", "178.175.129.252"]
    host = "EXHENTAI.ORG"
    r = IPcheck(ips, host).run()
    print(r)
