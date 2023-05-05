import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import re
from tqdm import tqdm

dict = {}
text = []
label = []
date = []

driver = webdriver.Firefox()

start_urls = []
article_urls = []
subjects = ['web', 'panorama', 'ausland', 'wirtschaft', 'sport', 'inland', 'etat', 'wissenschaft', 'kultur']
for s in subjects:
    for r in range(1,2):
        start_urls.append(f'http://www.tagesschau.de/suche#/article/{r}/?searchText={s}')

for link in tqdm(start_urls, desc='Get link to each article'):
    driver.get(link)
    time.sleep(2)
    links = driver.find_elements(By.XPATH, '//a[@class="teaser-right__link"]')
    for l in links:
        url = l.get_attribute('href')
        if url and (url not in article_urls):
            if 'newsticker/liveblog' not in url:
                article_urls.append(url)
                dict[url] = re.findall(r'=([^=]+)$', link)[0]
            else:
                pass
        else:
            pass

for u in tqdm(article_urls, desc='Parse articles'):
    if u:
        driver.get(u)
        article_text = driver.find_elements(By.XPATH, '//article//p[starts-with(@class, "textabsatz")]')
        article_text = [absatz.text for absatz in article_text]
        article_text = ''.join(article_text)
        article_text = re.sub(r'\n{2, }|\s{2,}', '', article_text)
        text.append(article_text)
        label.append(dict[u])
        try:
            article_timestamp = driver.find_element(By.XPATH, '//p[@class="metatextline"]').text
            match = re.search(r'\d{2}.\d{2}.\d{4}', article_timestamp)
            date.append(match.group(0))
        except NoSuchElementException:
            date.append(np.nan)
    else:
        pass

df = pd.DataFrame({'Text': text, 'Label': label, 'Date': date, 'Link': article_urls}).reset_index(drop=True)
df.to_csv('tagesschau.csv', index=False)

driver.quit()