import csv
import pandas as pd

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

htmlTable = '''<tr><th align="left" style="border-top-color: #808080;border-top-style:solid;border-top-width: 1px "></th><td style="border-top-color: #808080;border-top-style:solid;border-top-width: 1px"></td></tr><tr><th>Result #1</th><td></td></tr><tr><th align="left"><b>API</b></th><td><b>31734158</b></td></tr><tr><th align="left">GIS WELL NUMBER</th><td>1</td></tr><tr><th align="left">GIS SYMBOL DESCRIPTION</th><td>Plugged Oil Well</td></tr><tr><th align="left">GIS LOCATION SOURCE</th><td>Operator reported location - Distances and Plat</td></tr><tr><th align="left">GIS LAT (NAD27)</th><td>32.257789</td></tr><tr><th align="left">GIS LONG (NAD27)</th><td>-102.003085</td></tr><tr><th align="left">GIS LAT (NAD83)</th><td>32.257905</td></tr><tr><th align="left">GIS LONG (NAD83)</th><td>-102.003503</td></tr><tr><td align="left"><a href="javascript:void window.open('https://rrcsearch3.neubus.com/esd3-rrc/api.php?function=GetWellLogs&amp;api_no=31734158' , '');">Well Logs</a></td><td align="left"><a href="javascript:void window.open('http://webapps.rrc.texas.gov/DP/publicQuerySearchAction.do?countyCode=317&amp;apiSeqNo=34158' , '', 'width=900,height=600,scrollbars=yes,resizable=yes');">Drilling Permits</a></td><td align="left"><a href="javascript:void window.open('GISViewer/html/disposalPermit.htm?apiNo=31734158' , '');">Disposal Permits</a></td></tr>'''
soup = BS(htmlTable, 'html.parser')

left_rows = [tr.findAll('th') for tr in soup.findAll('tr')[:-1]]
right_rows = [tr.findAll('td') for tr in soup.findAll('tr')[:-1]]

l=[]
r=[]

for i in left_rows:
    l.append([i[0].text])

for i in right_rows:
    r.append([i[0].text])

with open('table.csv', 'w') as writeFile:
    for num, row in enumerate(right_rows, start=0):
        writer = csv.writer(writeFile)
        writer.writerow([l[num][0], r[num][0]])






