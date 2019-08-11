from main import browser_setup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pyscreenshot as ImageGrab
from tableScrape import scrapeTable
from bs4 import BeautifulSoup as BS
import csv

def screenshot(id):
    im = ImageGrab.grab()
    im.save('screenshots/leaseID_{}.png'.format(str(id)))
    im.show()

def stage4(id):
    browser = browser_setup()
    browser.get('http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home')
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="leaseNoArgHndlr:12"]'))).send_keys(id)  # Block
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[6]/tbody/tr/td/form/table/tbody/tr[4]/td/table/tbody/tr[5]/td/table/tbody/tr/td/input[1]'))).click()
    #screenshot(id)
    recordsFoundLinks = scrapeTable(browser)
    input()


def scrapeTable(browser):
    table = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[6]/tbody/tr/td/form/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody')))
    links = table.find_elements_by_tag_name('a')
    returnList = []
    for i in links[12:]:
        returnList.append(i.get_attribute("href"))
        print(i.get_attribute("href"))


    return returnList

def downloadDocs(browser,url):
    browser.get(url)
    table = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[6]/tbody/tr/td/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td')))
    urls = table.find_elements_by_tag_name('a')

def downloadPDF(url, name):


    driver.get(url)

if __name__ == '__main__':
    id = 35729
    stage4(id)
    #downloadPDF('http://webapps.rrc.texas.gov/CMPL/viewPdfReportFormAction.do?method=cmplL1FormPdf&packetSummaryId=52821')
