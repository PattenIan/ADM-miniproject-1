import requests
import dill
from bs4 import BeautifulSoup
from datetime import datetime

def getPage():
    page = requests.get("https://web.archive.org/web/20150913224145/http://www.newyorksocialdiary.com/party-pictures")
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all()
    print(links)
    