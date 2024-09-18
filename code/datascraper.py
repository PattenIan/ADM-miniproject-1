import requests
import dill
import re
from bs4 import BeautifulSoup
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
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

    print(month_with_most_parties(links_date))

    print(get_trend(links_date))
    
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
    print(len(links))
    for link in links:
        if((link[1][0] == cutoff.year and link[1][1] < cutoff.month) or (link[1][0] < cutoff.year)):
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



    