from selenium import webdriver
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By

# Create a list with dates
delta = timedelta(days=1)
dates = [datetime.strptime('2023/01/01', '%Y/%m/%d'),
         datetime.strptime('2023/01/01', '%Y/%m/%d')]
date_list = []
while dates[0] <= dates[1]:
    date_list.append(dates[0].strftime('%Y/%m/%d'))
    dates[0] += delta

start_urls = [f'https://www.derstandard.at/international/{date}' for date in date_list]

driver = webdriver.Chrome()

for date in start_urls:
    driver.get(date)
    par = driver.find_elements(By.XPATH, '//div[@class="article-body"]/p')
    for p in par:
        print(p.text)