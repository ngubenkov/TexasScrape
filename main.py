from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyscreenshot as ImageGrab
from stage3 import OpenSecondPage
from bs4 import BeautifulSoup as BS
import csv
'''
https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25

selenium + beautifulsoup because it dynamic page
'''
def browser_setup():
    '''
    setup browser
    '''
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "/Users/frozmannik/Desktop/TEXAS"}
    chromeOptions.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(executable_path = 'files/chromedriver',
                               chrome_options = chromeOptions)  # fake Chrome browser mac
    # browser = webdriver.Chrome('C:\\Users\Frozm\PycharmProjects\\biologyScrapeData\\files\win\chromedriver.exe')
    return browser

def open_page(url):
    '''
    open browser and click
    '''
    browser = browser_setup()
    browser.get(url)
    try:
        btn_Magnifying_Glass = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rrcsearchButton"]')))
        #print(btn_Magnifying_Glass)
        btn_Magnifying_Glass.click() # opens search

        btn_Survey = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dijit_rrcGisAnchorMenuItem_7_text"]')))
        btn_Survey.click()
        inputData(browser, 'MARTIN', '37 T2N', '36')
        print("Close form")
        input()
        # identify wells
        btn_Identify = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "identifyButton"] / span[1]')))
        btn_Identify.click()
        btn_Wells = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "dijit_rrcGisAnchorMenuItem_0_text"]')))
        btn_Wells.click()
    except Exception as e:
        print(e)


    # click on well
    print("Click on well")
    input()


    # scrape tables
    table1 = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="printIdentifyWellDiv"]/table[1]/tbody')))

    contentOfTable1 = table1.get_attribute('innerHTML')
    scrapeTable(contentOfTable1)
    print("supposevly we have table 1")

    table2 = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="printIdentifyWellDiv"]/table[3]/tbody')))
    contentOfTable2 = table2.get_attribute('innerHTML')
    scrapeTable(contentOfTable2)
    print("supposevly we have table 2")
    input()

def identifyWell(browser):
    obj = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '// *[ @ id = "printIdentifyWellDiv"] / table[2] / tbody')))

    print(obj)
    #content =  # contents of that table
   # soup = BS(content, 'html5lib')
   # rows = [tr.findAll('td') for tr in soup.findAll('tr')]

def inputData(browser,country, block, section):
    '''

    '''
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="countySelect"]/tbody/tr/td[2]/div[1]'))).click() # select countries btn
    items = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dijitMenuItemLabel'))) # list of drop down items
    for _ in items:
        if country.upper() in _.get_attribute('innerHTML'):
            _.click()

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "blockID"]'))).send_keys(block) # Block
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "sectionID"]'))).send_keys(section) # Section
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "querySurveyButton_label"]'))).click() # Query button
    #WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="zoomCloseBtn"]/a/img'))).click() # close form

    #TODO: close SURVEY SEARCH form and add delay to zoom at location
    # screenshot(country, block, section) #dont use it now


def screenshot(country, block, section):
    im = ImageGrab.grab()
    im.save('screenshots/{}_{}_{}.png'.format(country, block, section))
    im.show()

def identifyWells():
    '''
    62B783 - color in selected area
    60AE41 - outside of area

    '''

def open_second_page(url):
    '''
    STEP 3 (doesn't work)
    '''
    browser = browser_setup()
    browser.get(url)
    try:
        leaseID= WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lease_numberTEXT"]')))
        leaseID.send_keys("38582")
        search = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="docSearchButton"]')))
        search.click()

        #// *[ @ id = "searchResults"] / tbody / tr[4] / td[10]

        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='searchResults']/tbody//td[contains(text(), 'POTENTIAL')]")))
        WebDriverWait(browser, 30)
        print(element)
        input()
    except Exception as error:
        print(str(error))


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

    for i in left_rows:
        try:
            l.append([i[0].text])
        except IndexError as e:
            l.append([""])

    for i in right_rows:
        try:
            r.append([i[0].text])
        except IndexError as e:
            r.append([""])

    title = title.replace('/', '_') # convert to proper name

    with open('{}.csv'.format(title), 'w') as writeFile:
        for num, row in enumerate(l, start=0):
            writer = csv.writer(writeFile)
            print(l[num][0] + " : " + r[num][0])
            writer.writerow([l[num][0], r[num][0]])
    writeFile.close()

def step_4(url):
    browser = browser_setup()
    browser.get(url)


if __name__ == '__main__':
    open_page("http://wwwgisp.rrc.texas.gov/GISViewer2/")
    #step_4("http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home")
    #OpenSecondPage().open_second_page("​https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")

