import requests
import dill
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

links = "https://web.archive.org/web/20150918040703/http://www.newyorksocialdiary.com/party-pictures?page=1"

def get_page_links(page_link):
    page = requests.get(page_link)
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all(class_="views-row")
    #print(links, "   ", len(links))
    #print("URL 1: ", get_link_date(links[0]))
    #print("URL 2: ", get_link_date(links[1]))
    #print("URL 3: ", get_link_date(links[2]))
    #print("URL 4: ", get_link_date(links[3]))
    #print("URL 5: ", get_link_date(links[4]))
    #return links

    #links_date = [get_link_date(link) for link in links]

    #print(filter_by_date(links=links_date))
    return links
    
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


def gather_all_links():
    page_links = []
    all_links = []
    filtered_links = []
    for page in range (1,25):
        page_link = "https://web.archive.org/web/20150918040703/http://www.newyorksocialdiary.com/party-pictures?page=" + str(page)
        page_links.append(page_link)
    
    
    for pl in range(0, len(page_link)):
        sleep_timer = 1
        all_links.append(get_page_links(page_links[pl]))
        if pl >= 15:
            sleep_timer = 10
        time.sleep(sleep_timer)
        
        print("link done")
    
    for link in all_links:
        filtered_links.append(filter_by_date(link))
    print(filtered_links) 
    
    