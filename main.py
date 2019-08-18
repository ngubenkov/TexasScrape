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


# TODO: save leaseID in list
leaseID = []
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

    hoverBtns(browser,section)


def inputData(browser,country, block, section):
    '''
    input data in search
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

def hoverBtns(browser,section):
    '''
    go throw all well on the map
    hover each btn
    :param browser:
    :return:
    '''
    wellMap = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="rrcGisViewerMap"]')))
    wellimages = wellMap.find_elements_by_tag_name('image')
    wells = 0

    for image in wellimages:
        try:
            hover = ActionChains(browser).move_to_element(image)
            hover.perform()
            time.sleep(1)
            descriptionForm = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'dijitTooltipContainer')))
            br = descriptionForm.find_element(By.CLASS_NAME,"dijitTooltipFocusNode")
            if '"{}"'.format(section) in br.text[br.text.find('Lease Name :'):br.text.find('On Schedule :')]:
                print("FOUND ")
                wells += 1
                image.click()
                time.sleep(3)
                scrapePopUp(browser,image)

        except:
            print(" Acceptable shit happened")
            pass
    print("TOTAL WELLS {}".format(wells))

def scrapePopUp(browser,image):
    tbodys = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'esriPopupWrapper'))).find_elements_by_tag_name('tbody')
    print("FOUND POP UP ")
    count = 0
    for item in tbodys:
        count += 1
        try:
            tableContent = item.get_attribute('innerHTML')
            scrapeTable(tableContent)
            print("TABLE SCRAPED SUCCESSFULLY {}".format(count))
        except:
            print("NON ACCEPTABLE SHIT HAPPENED CANT SCRAPE Table {}".format(count))

    while True:
        try:
            WebDriverWait(browser, 10).until(  # close form
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="rrcGisViewerMap_root"]/div[3]/div[1]/div[1]/div/div[6]'))).click()
            break
        except:
            print("cant close pop up (PROBABLY MOVE MOUSE A BIT)")
            ac = ActionChains(browser)
            ac.move_to_element(image).move_by_offset(5, 5).click().perform()
            break


if __name__ == '__main__':
    open_page('MARTIN', '37 T2N', '36')
    #step_4("http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home")
    #OpenSecondPage().open_second_page("​https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")

