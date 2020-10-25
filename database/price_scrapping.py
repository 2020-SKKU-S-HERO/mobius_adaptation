#!/usr/bin/env python
# coding: utf-8
#import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver',options=chrome_options)
driver.get('https://ets.krx.co.kr/contents/ETS/03/03010000/ETS03010000.jsp')
time.sleep(10)
driver.implicitly_wait(1000)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

price_info = []
for i in range(1,9):
	price_info.append(soup.select('.design-table1 > table > thead + tbody > tr:FIRST-CHILD > td')[i])
print(price_info)


driver.quit()
