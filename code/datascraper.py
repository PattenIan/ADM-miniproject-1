import requests
import dill
import re
from bs4 import BeautifulSoup
from datetime import datetime

links = set

def getPage():
    page = requests.get("https://web.archive.org/web/20150913224145/http://www.newyorksocialdiary.com/party-pictures")
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all(class_="views-row")
    print(links, "   ", len(links))
    print("URL maybe?: ", get_link_date(links[0]))
    
def get_link_date(link):
    titleField = link.find(class_="views-field-title")
    url = titleField.find("a")['href'] if titleField else None
    pattern = r'.?(http[s]?://.)'
    result = re.sub(pattern, r'\1', url)
    return result
    