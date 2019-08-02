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
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "/Users/frozmannik/Desktop/TEXAS"}
    chromeOptions.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(executable_path = '/Users/frozmannik/PycharmProjects/TexasScrape/files/chromedriver',
                               chrome_options = chromeOptions)  # fake Chrome browser mac
    # browser = webdriver.Chrome('C:\\Users\Frozm\PycharmProjects\\biologyScrapeData\\files\win\chromedriver.exe')
    return browser



def duno():
    '''dont need this code'''
    url = "http://wwwgisp.rrc.texas.gov/GISViewer2/"
    crawl_url = get(url, headers={'User-Agent': 'Mozilla/5.0'})
    crawl_url.raise_for_status()
    soup = BeautifulSoup(crawl_url.text)
    print(soup)

def open_page(url):
    browser = browser_setup()
    browser.get(url)
    try:
        buttons = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.ID, "rrcsearchButton")))
        print(buttons)
        buttons[0].click() # opens search
        input()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    open_page("http://wwwgisp.rrc.texas.gov/GISViewer2/")