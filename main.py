from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
        inputData(browser)
        input()
    except Exception as e:
        print(e)

def inputData(browser,country=None, block=None, section=None):
    ''' [ dijitReset ] is drop down element contains all counties
      path should be somethin like :   [ dijitReset ] / [dijitReset dijitMenuItem] / [dijitReset dijitMenuItemLabel] [ inner HTML ]
    '''
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="countySelect"]/tbody/tr/td[2]/div[1]'))).click() # select countries btn
    items = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dijitMenuItemLabel'))) # list of drop down items
    for _ in items:
        #print(_.get_attribute('innerHTML'))
        if 'MARTIN' in _.get_attribute('innerHTML'):
            print("FAMUTON")
            print(_.get_attribute('innerHTML'))
            _.click()

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "blockID"]'))).send_keys('37 T2N') # Block

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "sectionID"]'))).send_keys('36') # Section

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "querySurveyButton_label"]'))).click() # Query button



if __name__ == '__main__':
    '''
    test input is : County: Martin, Block: 37 T2N, Section: 36

    '''
    open_page("http://wwwgisp.rrc.texas.gov/GISViewer2/")

