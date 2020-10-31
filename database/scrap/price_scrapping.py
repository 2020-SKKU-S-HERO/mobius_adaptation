#!/usr/bin/env python
# coding: utf-8
#import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver',options=chrome_options)
driver.implicitly_wait(100)
driver.get('https://ets.krx.co.kr/contents/ETS/03/03010000/ETS03010000.jsp')
time.sleep(6)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

price_info = []
for i in range(1,9):
	price_info.append(soup.select('.design-table1 > table > thead + tbody > tr:FIRST-CHILD > td')[i].text)
print(price_info)

driver.quit()
