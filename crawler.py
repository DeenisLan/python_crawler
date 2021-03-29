#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import os 
import sys 
import pandas as pd

raw_request = Request('https://stock.wespai.com/rate110')
raw_request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0')
raw_request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
resp = urlopen(raw_request)
raw_html = resp.read()
soup = BeautifulSoup(raw_html,"html.parser")

tables = soup.findAll("table")
list_header = [] 
header = soup.find_all("table")[0].find("tr") 

past_request = Request('https://stock.wespai.com/rate109')
past_request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0')
past_request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
resppast = urlopen(past_request)
past_html = resppast.read()
souppast = BeautifulSoup(past_html,"html.parser")

pasttables = souppast.findAll("table")

for items in header: 
    try: 
        list_header.append(items.get_text()) 
    except: 
        continue

tableMatrix = []
for table in tables:
    #Here you can do whatever you want with the data! You can findAll table row headers, etc...
    list_of_rows = []
    for row in table.findAll('tr')[1:]:
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    tableMatrix = list_of_rows
# print(tableMatrix)
# DataFrame  
dataFrame = pd.DataFrame(data = tableMatrix, columns = list_header) 
# print(dataFrame['代號'])
# print(list_of_rows[0][0])

tableMatrix = []
for table in pasttables:
    #Here you can do whatever you want with the data! You can findAll table row headers, etc...
    list_of_rows = []
    for row in table.findAll('tr')[1:]:
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        if list_of_cells[0] not in dataFrame['代號']:
            list_of_rows.append(list_of_cells)
    tableMatrix = list_of_rows
# print(tableMatrix)
# Converting Pandas DataFrame 
# into CSV file 
dataFrame.to_csv('~/Desktop/today.csv', encoding='utf_8_sig')