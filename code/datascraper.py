import requests
import dill
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
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

links = "https://web.archive.org/web/20150918040703/http://www.newyorksocialdiary.com/party-pictures?page=1"

    
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
    print(len(links))
    for link in links:
        url, date = link
        
        # Check if the URL and date exist and date is valid
        if date and url and (date[0] < cutoff.year or (date[0] <= cutoff.year and date[1] < cutoff.month) or (date[0] == cutoff.year and date[1] == cutoff.month and date[2] == cutoff.day)):
            filtered.append(link)
    
    return filtered

def month_with_most_parties(links) -> str:
    months = [0] * 12
    for link in links:
        print(link)
        months[link[1][1] - 1] += 1

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    max = 0
    max_index = []
    print(months)
    for i in range(12):
        if months[i] > max:
            max = months[i]
            max_index.clear()
            max_index.append(i)
        elif months[i] == max:
            max_index.append(i)

    return [month_names[i] for i in max_index]

def get_trend(links):
    dates = [link[1] for link in links]
    dates_as_datetime = [datetime(year, month, day) for year, month, day in dates]

    dates_by_month = [date.strftime('%Y-%m') for date in dates_as_datetime]
    occurrences = Counter(dates_by_month)

    # Create a DataFrame to fill in missing months from 2007 to 2014
    all_months = pd.date_range(start='2007-01', end='2014-12', freq='M').strftime('%Y-%m')
    df = pd.DataFrame(all_months, columns=['YearMonth'])
    df['Occurrences'] = df['YearMonth'].map(occurrences).fillna(0)

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['YearMonth'], df['Occurrences'], marker='o', color='b', label='Occurrences per Month')
    plt.xticks(rotation=90)
    plt.xlabel('Month')
    plt.ylabel('Occurrences')
    plt.title('Occurrences per Month from 2007 to 2014')
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()



def month_with_most_parties(links) -> str:
    months = [0] * 12
    for link in links:
        print(link)
        months[link[1][1] - 1] += 1

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    max = 0
    max_index = []
    print(months)
    for i in range(12):
        if months[i] > max:
            max = months[i]
            max_index.clear()
            max_index.append(i)
        elif months[i] == max:
            max_index.append(i)

    return [month_names[i] for i in max_index]

def get_trend(links):
    dates = [link[1] for link in links]
    dates_as_datetime = [datetime(year, month, day) for year, month, day in dates]

    dates_by_month = [date.strftime('%Y-%m') for date in dates_as_datetime]
    occurrences = Counter(dates_by_month)

    # Create a DataFrame to fill in missing months from 2007 to 2014
    all_months = pd.date_range(start='2007-01', end='2014-12', freq='M').strftime('%Y-%m')
    df = pd.DataFrame(all_months, columns=['YearMonth'])
    df['Occurrences'] = df['YearMonth'].map(occurrences).fillna(0)

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['YearMonth'], df['Occurrences'], marker='o', color='b', label='Occurrences per Month')
    plt.xticks(rotation=90)
    plt.xlabel('Month')
    plt.ylabel('Occurrences')
    plt.title('Occurrences per Month from 2007 to 2014')
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    plt.show()



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
    
def get_captions(page_link, is_photocaption):
    try:
        page_content = requests.get(page_link)
        soup = BeautifulSoup(page_content.text, "lxml")
        
        if is_photocaption:
            captions = soup.find_all(class_="photocaption")
        else:
            captions = soup.find_all('font', attrs={
                'size': '1',
                'face': 'Verdana, Arial, Helvetica, sans-serif'
            })
        
        return captions
    except Exception as e:
        print(f"Error fetching page {page_link}: {e}")
        return []


def clean_captions(captions):
    delete_character = False
    cleaned_captions = []

    for caption in captions:
        clean_caption = ""  # Reset clean_caption for each caption
        for character in str(caption):  # Convert caption to a string
            if character == '<':
                delete_character = True
            elif character == '>':
                delete_character = False
                continue  # Skip appending the '>' character
            if not delete_character:
                clean_caption += character

        if not clean_caption.isspace():
            cleaned_captions.append(clean_caption)
        
    return cleaned_captions

import time

def get_all_captions():
    link_list = dill.load(open('nysd-links.pkd', 'rb'))
    cutoff = datetime(2007, 9, 4)
    with open('All_Captions.txt', 'a', encoding='utf-8') as f:
        for link, date in link_list:
            print(date)

            link = "https://web.archive.org/web/20151024130444/" + link
            
            print(f"Processing: {link}")
            failed_link_list = []
            success = False
            retries = 3  # Number of retries
            
            for attempt in range(retries):
                try:
                    if (date[0] < cutoff.year or 
                    (date[0] <= cutoff.year and date[1] < cutoff.month) or 
                    (date[0] == cutoff.year and date[1] == cutoff.month and date[2] == cutoff.day)):
                        captions = get_captions(link, False)
                    else:
                        captions = get_captions(link, True)
                    print(f"Captions fetched successfully")
                    success = True
                    break  # Exit retry loop on success

                except Exception as e:
                    print(f"Error fetching captions from {link} on attempt {attempt+1}")
                    time.sleep(5*attempt)  # Wait 2 seconds before retrying
            
            if not success:
                failed_link_list.append(link, date)
            else:
                clean_cap = clean_captions(captions)
                for caption in clean_cap:
                    caption = str(caption)
                    f.write(caption)
    f.close()



"""
[^,]+?(?=(?:,| and|$))
(?<=and\s)(.*)
(.*?)(?=\s+at\b)
"""
