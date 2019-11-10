import csv
from bs4 import BeautifulSoup as BS
import os

def scrapeTable(htmlTable, dict_table):
    ''' Scrape html table object
    input:
    '''
    soup = BS(htmlTable, 'html.parser')
    left_rows = [tr.findAll('th') for tr in soup.findAll('tr')[:]]
    right_rows = [tr.findAll('td') for tr in soup.findAll('tr')[:]]

    for index , key in enumerate(left_rows):
        if key:
            dict_table[key[0].text] = right_rows[index][0].text if right_rows[index] else ''
        else:
            dict_table['empty'+str(index)] = right_rows[index][0].text if right_rows[index][0].text else ''
    return dict_table


def save_well_attribute(folder, dict_table):

    if not os.path.exists(folder):
        print("@@@@@@@@@@")
        os.makedirs(folder)
        print("MAKE DIR")
    else:
        print("FUCK YOU")
    dict_table.pop('')
    with open(folder + "/Well_Attributes.csv", 'w') as writeFile:
        for key, value in dict_table.items():
            writer = csv.writer(writeFile)
            if str(key).startswith('empty'):
                key=''
            writer.writerow([key,value])