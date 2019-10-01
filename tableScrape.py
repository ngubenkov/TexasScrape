import csv
from bs4 import BeautifulSoup as BS
import os

def scrapeTable(htmlTable, mainFolder, folderInd):
    ''' Scrape html table object
    input:
    '''
    soup = BS(htmlTable, 'html.parser')

    left_rows = [tr.findAll('th') for tr in soup.findAll('tr')[:]]
    right_rows = [tr.findAll('td') for tr in soup.findAll('tr')[:]]

    # sometimes table has first row empty
    if left_rows[0][0].text != "":
        title = left_rows[0][0].text
    else:
        title = left_rows[1][0].text

    l = []
    r = []

    ind = 0
    idInd = None
    for i in left_rows:
        try:
            l.append([i[0].text])
            if 'LEASE/ID' in i[0].text:
                idInd = ind
        except IndexError as e:
            l.append([""])

        ind += 1

    for i in right_rows:
        try:
            r.append([i[0].text])
        except IndexError as e:
            r.append([""])

    title = title.replace('/', '_') # convert to proper name

    print("HERE 1")
    print(title)
    print(folderInd)
    if not os.path.exists(mainFolder + "/{}".format(folderInd)):
        os.makedirs(mainFolder + "/{}".format(folderInd))

    print("HERE 222")

    try: # works fine for table 2
        print("save file " + "save file " + mainFolder + "/" + str(folderInd) + "/{}.csv".format(title))
        with open(mainFolder + "/" + str(folderInd) + "/{}.csv".format(title), 'w') as writeFile:
            for num, row in enumerate(l, start=0):
                writer = csv.writer(writeFile)
                # print(l[num][0] + " : " + r[num][0])
                writer.writerow([l[num], r[num]])

        writeFile.close()

        try:
            return str(r[idInd])
        except:
            print("CANNOT RETURN LEASE ID")
            return None

    except Exception as e:
        print(str(e))




