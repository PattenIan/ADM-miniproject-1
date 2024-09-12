import requests
import dill
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

def get_page_links(page_link):
    try:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.text, "lxml")
        
        # Find all rows containing links and dates
        rows = soup.find_all(class_="views-row")
        
        # Store the (url, date) tuples
        links_and_dates = [get_link_date(row) for row in rows]
        
        return links_and_dates
    except Exception as e:
        print(f"Error fetching page {page_link}: {e}")
        return []

def get_link_date(link):
    try:
        # Extract the URL from the title field
        titleField = link.find(class_="field-content")
        url = titleField.find("a")['href'] if titleField and titleField.find("a") else None
        pattern = r'^.*?(http)'
        cleaned_url = re.sub(pattern, r'\1', url) if url else None
        
        # Extract the date from the created field
        dateField = link.find(class_="views-field-created")
        date_str = dateField.find(class_="field-content").text if dateField else None
        
        # Convert the date string to a tuple (year, month, day)
        date = convert_date(date_str) if date_str else None
        
        return (cleaned_url, date)
    except Exception as e:
        print(f"Error processing link: {e}")
        return (None, None)

def convert_date(date_str):
    try:
        input_format = "%A, %B %d, %Y"
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.year, date_obj.month, date_obj.day
    except Exception as e:
        print(f"Error converting date '{date_str}': {e}")
        return None

def filter_by_date(links, cutoff=datetime(2014, 12, 1)):
    filtered = []
    for link in links:
        url, date = link
        
        # Check if the URL and date exist and date is valid
        if date and url and (date[0] < cutoff.year or (date[0] <= cutoff.year and date[1] < cutoff.month) or (date[0] == cutoff.year and date[1] == cutoff.month and date[2] == cutoff.day)):
            filtered.append(link)
    
    return filtered

def gather_all_links():
    page_links = []
    all_links = []
    filtered_links = []
    
    # Generate the page URLs
    for page in range(1, 26):
        page_link = f"https://web.archive.org/web/20150918040703/http://www.newyorksocialdiary.com/party-pictures?page={page}"
        page_links.append(page_link)
    
    # Fetch links from each page
    for pl in range(0, len(page_links)):
        sleep_timer = 10
        page_links_data = get_page_links(page_links[pl])
        all_links.extend(page_links_data)
        
        time.sleep(sleep_timer)
        
        print(f"Page {pl + 1} done")
    
    # Filter links by date
    filtered_links = filter_by_date(all_links)
    
    # Save the filtered links
    dill.dump(filtered_links, open('nysd-links.pkd', 'wb'))
    print(f"Filtered links: {filtered_links}")
    print("Amount of links: ", len(filtered_links))
