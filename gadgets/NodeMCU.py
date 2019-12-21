import requests


class NodeMCU:
    def __init__(self, ip):
        self.url = "http://" + ip

    def send(self, pin, value):
        requests.get(f"{self.url}/digital/{pin}/{value}")
