import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Scraper(object):
    def __init__(self, confing):
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
        self.url = confing["source_url"]
    def __call__(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, "html.parser")
        table = [[td.text for td in tr.find_all("td")] for tr in soup.find("table", class_="commontbl").find_all("tr")]
        return [{
            "right_last_date": datetime.strptime(tr[0], "%Y-%m-%d").date(),
            "symbol_code": tr[1],
            "ratio": float(tr[6])
            } for tr in table if len(tr) > 0]
