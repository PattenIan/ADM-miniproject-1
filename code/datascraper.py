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
    #print(links, "   ", len(links))
    print("URL 1: ", get_link_date(links[0]))
    print("URL 2: ", get_link_date(links[1]))
    print("URL 3: ", get_link_date(links[2]))
    print("URL 4: ", get_link_date(links[3]))
    print("URL 5: ", get_link_date(links[4]))
    
def get_link_date(link):
    titleField = link.find(class_="field-content")
    url = titleField.find("a")['href'] if titleField else None
    pattern = r'^.*?(http)'
    cleaned_url = re.sub(pattern, r'\1', url)
    
    dateField = link.find(class_="views-field-created")
    date = dateField.find(class_="field-content").text if dateField else None
    
    return cleaned_url, date
    