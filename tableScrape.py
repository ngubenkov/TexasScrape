import csv
import pandas as pd

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def scrapeTable(htmlTable):
    soup = BS(htmlTable, 'html.parser')

    left_rows = [tr.findAll('th') for tr in soup.findAll('tr')[1:-1]]
    right_rows = [tr.findAll('td') for tr in soup.findAll('tr')[1:-1]]

    print((left_rows[0][0]).text)
    title = left_rows[0][0].text
    print(title)
    left_rows = left_rows[1:]
    l = []
    r = []

    for i in left_rows:
        l.append([i[0].text])

    for i in right_rows:
        r.append([i[0].text])

    with open('{}.csv'.format(title), 'w') as writeFile:
        for num, row in enumerate(right_rows, start=0):
            writer = csv.writer(writeFile)
            writer.writerow([l[num][0], r[num][0]])

    writeFile.close()






