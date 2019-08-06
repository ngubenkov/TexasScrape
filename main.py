from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyscreenshot as ImageGrab
from bs4 import BeautifulSoup as BS

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

    browser = webdriver.Chrome(executable_path = '/Users/frozmannik/PycharmProjects/TexasScrape/files/chromedriver',
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
        input()
        # identify wells
        btn_Identify = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "identifyButton"] / span[1]')))
        btn_Identify.click()
        btn_Wells = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "dijit_rrcGisAnchorMenuItem_0_text"]')))
        btn_Wells.click()
        input()
        # click on well
        print("hERE")
        obj = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="printIdentifyWellDiv"]/table[2]/tbody')))

        print(obj.get_attribute('innerHTML'))
        content = obj.get_attribute('innerHTML')
        soup = BS(content, 'html.parser')
        rows = [tr.findAll('td') for tr in soup.findAll('tr')]
        print(rows)
        for it in rows:
            with open('result.csv', 'a') as f:
                f.write(", ".join(str(e).replace('<td>', '').replace('</td>', '') for e in it) + '\n')
        input()
    except Exception as e:
        print(e)

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
        #print(_.get_attribute('innerHTML'))
        if country.upper() in _.get_attribute('innerHTML'):
            print("found")
            print(_.get_attribute('innerHTML'))
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
                (By.XPATH, "//*[@id='searchResults']/tbody//td[contains(text(), 'POTENTIAL')]"))
        )
        WebDriverWait(browser, 30)
        print(element)
        input()
    except Exception as error:
        print(str(error))


def step_4(url):
    browser = browser_setup()
    browser.get(url)


if __name__ == '__main__':
    open_page("http://wwwgisp.rrc.texas.gov/GISViewer2/")
    #step_4("http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home")
   # open_second_page("​https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")


