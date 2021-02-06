import requests


class NodeMCU:
    def __init__(self, ip):
        self.url = "http://" + ip

    def send(self, path):
        try:
            requests.get(f"{self.url}/{path}", timeout=1)
            return True
        except:
            return False
