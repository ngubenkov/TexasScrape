from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyscreenshot as ImageGrab
from tableScrape import scrapeTable
import time
from selenium.webdriver.common.action_chains import ActionChains
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
    download_dir = "/Users/frozmannik/PycharmProjects/TexasScrape/pdf"  # for linux/*nix, download_dir="/usr/Public"
    options = webdriver.ChromeOptions()

    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],  # Disable Chrome's PDF Viewer
               "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"}
    options.add_experimental_option("prefs", profile)
    browser = webdriver.Chrome('files/chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.
    return browser

def open_page(country, block, section):
    '''
    open browser and click
    '''
    url = "http://wwwgisp.rrc.texas.gov/GISViewer2/"
    browser = browser_setup()
    browser.get(url)
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rrcsearchButton"]'))).click()
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dijit_rrcGisAnchorMenuItem_7_text"]'))).click()

        inputData(browser, country, block, section)
        # identify wells
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "identifyButton"] / span[1]'))).click()
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "dijit_rrcGisAnchorMenuItem_0_text"]'))).click()

    except Exception as e:
        print(e)



    hoverBtns(browser)
    # scrape tables


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
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#fpSurveySearch #zoomCloseBtn a img'))).click()  # close form
    time.sleep(5)
    screenshot(country, block, section)  # dont use it now

def screenshot(country, block, section):
    im = ImageGrab.grab()
    im.save('screenshots/{}_{}_{}.png'.format(country, block, section))
    #im.show()

def open_second_page(url):
    '''
    STEP 3 (doesn't work)
    '''
    browser = browser_setup()
    browser.get(url)
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lease_numberTEXT"]'))).send_keys("38582")
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="docSearchButton"]'))).click()

        element = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='searchResults']/tbody//td[contains(text(), 'POTENTIAL')]")))
        WebDriverWait(browser, 30)
        print(element)
        input()
    except Exception as error:
        print(str(error))


def step_4(url):
    browser = browser_setup()
    browser.get(url)


def hoverBtns(browser):
    '''
    go throw all well on the map
    hover each btn
    :param browser:
    :return:
    '''
    wellMap = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="rrcGisViewerMap"]')))
    wellimages = wellMap.find_elements_by_tag_name('image')
    for image in wellimages:
        try:
            hover = ActionChains(browser).move_to_element(image)
            hover.perform()
            time.sleep(1)
            descriptionForm = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'dijitTooltipContainer')))
            br = descriptionForm.find_element(By.CLASS_NAME,"dijitTooltipFocusNode")
            if 'WOODY "36"' in br.text:
                print("FOUND")
                image.click()
                scrapePopUp(browser)
                input()
        except:
            print("shit happened")
            pass

def scrapePopUp(browser):
    table1 = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="printIdentifyWellDiv"]/table[1]/tbody')))

    contentOfTable1 = table1.get_attribute('innerHTML')
    scrapeTable(contentOfTable1)


    table2 = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="printIdentifyWellDiv"]/table[3]/tbody')))
    contentOfTable2 = table2.get_attribute('innerHTML')
    scrapeTable(contentOfTable2)

    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="rrcGisViewerMap_root"]/div[3]/div[1]/div[1]/div/div[6]'))).click()

    input()

if __name__ == '__main__':
    open_page('MARTIN', '37 T2N', '36')
    #step_4("http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home")
    #OpenSecondPage().open_second_page("​https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")



'M 348,535 331,540 294,395 294,395 230,145 248,140 362,109 362,109 631,35 730,395 730,395 738,424 348,535'
'M 348 535 331 540 294 395 294 395 230 145 248 140 362 109 362 109 631 35 730 395 730 395 738 424 348 535'

