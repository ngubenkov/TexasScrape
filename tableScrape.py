import csv
from bs4 import BeautifulSoup as BS

def scrapeTable(htmlTable):
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
            print(i[0].text)
            if 'LEASE/ID' in i[0].text:
                print("FOUND LEASE ID AT POSITION")
                print(str(ind))
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
    print("save file {}_{}.csv".format(title,str(r[idInd])))
    with open('{}_{}.csv'.format(title,str(r[idInd])), 'w') as writeFile:
        for num, row in enumerate(l, start=0):
            writer = csv.writer(writeFile)
            #print(l[num][0] + " : " + r[num][0])
            writer.writerow([l[num][0], r[num][0]])

    writeFile.close()


    try:
        return str(r[idInd])

    except:
        print("CANNOT RETURN LEASE ID")
        return None



