#!/usr/bin/env python
# coding: utf-8
import time
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:\Projects\Mobius\chromedriver_win32\chromedriver')
driver.get('https://ets.krx.co.kr/contents/ETS/03/03010000/ETS03010000.jsp')
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

price_info = []
for i in range(1,9):
    price_info.append(soup.select('.design-table1 > table > thead + tbody > tr:FIRST-CHILD > td')[i].text)

print(price_info)
