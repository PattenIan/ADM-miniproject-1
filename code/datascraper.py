import requests
import dill
import re
from bs4 import BeautifulSoup
from datetime import datetime

links = "https://web.archive.org/web/20150918040703/http://www.newyorksocialdiary.com/party-pictures?page=1"

def get_page_links():
    page = requests.get("https://web.archive.org/web/20150918040703/http://www.newyorksocialdiary.com/party-pictures?page=1")
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all(class_="views-row")
    #print(links, "   ", len(links))
    print("URL 1: ", get_link_date(links[0]))
    print("URL 2: ", get_link_date(links[1]))
    print("URL 3: ", get_link_date(links[2]))
    print("URL 4: ", get_link_date(links[3]))
    print("URL 5: ", get_link_date(links[4]))
    #return links

    links_date = [get_link_date(link) for link in links]

    print(filter_by_date(links=links_date))
    
def get_link_date(link):
    titleField = link.find(class_="field-content")
    url = titleField.find("a")['href'] if titleField else None
    pattern = r'^.*?(http)'
    cleaned_url = re.sub(pattern, r'\1', url)
    
    dateField = link.find(class_="views-field-created")
    date = dateField.find(class_="field-content").text if dateField else None
    
    return cleaned_url, convert_date(date)

def convert_date(date_str):
    input_format = "%A, %B %d, %Y"

    date_obj = datetime.strptime(date_str, input_format)

    return date_obj.year, date_obj.month, date_obj.day

def filter_by_date(links, cutoff=datetime(2014, 12, 1)):
    filtered = []
    for link in links:
        if(link[1][0] <= cutoff.year and link[1][1] < cutoff.month):
            filtered.append(link)
    return filtered

    