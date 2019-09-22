import csv
from bs4 import BeautifulSoup as BS
import os

def scrapeTable(htmlTable, mainFolder, pl = None, pr=None):
    ''' Scrape html table object
    input:
    '''
    print("SCRAPE")
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

    if not pl and not pr:
        return l,r, None
    else:
        pl.extend(l)
        pr.extend(r)
        title = title.replace('/', '_') # convert to proper name
        if idInd:
            fileName = mainFolder+"/"+str(r[2][0])+"/{}_{}.csv".format(title,str(r[idInd][0]))
            print("save file " + fileName)
        else:
            fileName =  mainFolder + "/" + str(r[2][0]) + "/{}.csv".format(title)
            print("save file " + fileName)
        print("TABLE")
        print(htmlTable)
        print("MB CORRECT TABLE")
        print(soup)


        input()
        # TODO: doesnt create folder
        if not os.path.exists(mainFolder+"/"+str(r[2][0])):
            print("@@@@@@@@@@")
            os.makedirs(mainFolder+"/"+str(r[2][0]))
            print("MAKE DIR")
        else:
            print("FUCK YOU")

        with open(fileName, 'w') as writeFile:
            for num, row in enumerate(l, start=0):
                writer = csv.writer(writeFile)
                writer.writerow([l[num][0], r[num][0]])

        writeFile.close()

        try:
            return str(r[idInd][0])

        except:
            print("CANNOT RETURN LEASE ID")
            return None



