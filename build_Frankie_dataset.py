# importing packages

import requests
from bs4 import BeautifulSoup
import time
import pickle
from tqdm import tqdm
import pandas as pd
import numpy as np

TodaysDate = time.strftime("%Y-%m-%d")

def retrieve_news_hyperlinks(main_url):
    """ 
    Extract all hyperlinks in 'main_url' and return a list with these hyperlinks 
    """
    
    # Packages the request, send the request and catch the response: r
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    
    # Packages the request, send the request and catch the response: r
    
    r = requests.get(main_url, headers=headers)
    
    # Create a BeautifulSoup object from the HTML: soup
    
    soup = BeautifulSoup(r.text,"lxml")
    
    # Find all 'a' tags (which define hyperlinks): a_tags

    a_tags = soup.find_all('a')

    # Create a list with hyperlinks found

    list_links = [link.get('href') for link in a_tags]
    
    # keep only news links (i.e. containing "?ifcn_misinformation")
    
    list_news = [link for link in list_links if "?ifcn_misinformation" in link]
    
    # remove duplicates
    
    list_news = list(set(list_news))
    
    # Remove none values if there is some
    
    list_news = list(filter(None, list_news)) 
    
    return list_news

def build_csv(list_news_urls):
    """ 
    Build csv with extract information of hyperlinks in list of hyperlinks of Poynter.
    
    """
    
    #list of information extract from website
    
    fact_checker = []
    date = []
    location = []
    label = []
    title = []
    explanation = []
    claim_originated_by = []
    url_checker = []
    
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        
    for idx in tqdm(range(len(list_news_urls))):
        
        r = requests.get(list_news_urls[idx], headers=headers)
    
        # Create a BeautifulSoup object from the HTML: soup
        soup = BeautifulSoup(r.text,"lxml")

        fact_checker.append(soup.find('p', class_='entry-content__text entry-content__text--org').get_text().split(':')[-1].strip())

        date_location = soup.find('p', class_="entry-content__text entry-content__text--topinfo").get_text()
    
        date.append(date_location.split('|')[-2])

        location.append(date_location.split('|')[-1].strip())

        label_title = soup.find("h1",class_="entry-title").get_text()

        label.append(label_title.split(":")[0].replace("\n","").strip().lower())

        title.append(label_title.split(":")[1].replace("\t\t","").strip())

        explanation.append(soup.find('p',class_="entry-content__text entry-content__text--explanation").get_text().split(":")[1].strip())

        claim_originated_by.append(soup.find('p', class_="entry-content__text entry-content__text--smaller").get_text().split(":")[1].strip())

        url_checker.append(soup.find('a', class_="button entry-content__button entry-content__button--smaller").get("href"))

    dict_info = {'fact_checker':fact_checker,
                 'date':date, 
                 'location': location,
                 'label':label,
                 'title':title,
                 'explanation':explanation,
                 'claim_originated_by':claim_originated_by,
                 'url_checker':url_checker}
    
    df = pd.DataFrame(dict_info)

    return df


# url from poynter

main_url = "https://www.poynter.org/ifcn-covid-19-misinformation/?orderby=views&order=DESC#038;order=DESC"

# retrieve all hyperlinks from all 308 pages with corona news 

all_news_links = retrieve_news_hyperlinks(main_url)

for page in tqdm(range(309)):
    if page == 0:
        all_news_links = retrieve_news_hyperlinks(main_url)
    else:     
        all_news_links.extend(retrieve_news_hyperlinks("https://www.poynter.org/ifcn-covid-19-misinformation/page/"+str(page)+"/?orderby=views&order=DESC#038;order=DESC"))
        
# Build dataset using hyperlinks retrieved

df = build_csv(all_news_links)

# saving in csv

df.to_csv("./data/data_poynter_COMPLETE_"+TodaysDate+".csv", index=False)

# saving in excel

df.to_excel("./data/data_poynter_COMPLETE_"+TodaysDate+".xlsx")

