from collections import Counter
import numpy as np
import pandas as pd
import re
import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

# Datastructures
dict = {}
df_text = []
df_label = []
df_date = []
df_url = []

# Open webdriver
driver = webdriver.Firefox()

# Preparing
"""
We will create a list with 20 links to articles for each our subject.
There are 20 pages for each subject.
"""
start_urls = [] # 20 start pages for each subject
subjects = ['web', 'panorama', 'ausland', 'wirtschaft', 'sport', 'inland', 'etat', 'wissenschaft', 'kultur']
for s in subjects:
    for r in range(1, 21):
        start_urls.append(f'http://www.tagesschau.de/suche#/article/{r}/?searchText={s}')

# Get url for each news article found after iterating over each start page
article_urls = []
for link in tqdm(start_urls, desc='Get link to each article'):
    driver.get(link)
    time.sleep(2)
    links_selenium = driver.find_elements(By.XPATH, '//a[@class="teaser-right__link"]') # Get all links on each start page
    for elem in links_selenium:
        url = elem.get_attribute('href') # Convert to string
        if (url is not None) and (url not in article_urls): # If not empty and not already in our list
            if 'newsticker/liveblog' not in url: # Avoid liveblog pages
                article_urls.append(url) # Add link to our list
                dict[url] = re.findall(r'=([^=]+)$', link)[0] # Set link and subject as key value pair in our dictionary
            else:
                pass
        else:
            pass

# Show found links
print(f'\nLinks found: {len(article_urls)}'
      f'\nSubjects distribution: {Counter(dict.values())}\n')

# Parse articles to find text and date
for u in tqdm(article_urls, desc='Parse articles'):
    # If article exists
    if u:
        try:
            # Open article
            driver.get(u)

            # Get article text
            article_text = driver.find_elements(By.XPATH, '//article//p[starts-with(@class, "textabsatz")]')
            article_text = [absatz.text for absatz in article_text]
            article_text = ''.join(article_text)
            article_text = re.sub(r'\n{2, }|\s{2,}', '', article_text)

            # Add text, label, date and link to our dataframe lists
            df_text.append(article_text)
            df_label.append(dict[u])
            """
            Add date to our dataframe list. If system find the date, it will add it to or list,
            otherwise the system will put np.nan to our dataframe list
            """
            try:
                article_timestamp = driver.find_element(By.XPATH, '//p[@class="metatextline"]').text
                match = re.search(r'\d{2}.\d{2}.\d{4}', article_timestamp)
                df_date.append(match.group(0))
            except NoSuchElementException:
                df_date.append(np.nan)
            df_url.append(u)

        except selenium.common.exceptions.WebDriverException:
            pass
    else:
        pass

# Create dataframe with our lists and save it as CSV file
df = pd.DataFrame({'Text': df_text, 'Label': df_label, 'Date': df_date, 'Link': df_url}).reset_index(drop=True)
df.to_csv('tagesschau.csv', index=False)

# Close the webriver
driver.quit()