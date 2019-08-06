from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import pyscreenshot as ImageGrab

class OpenSecondPage:
    def browser_setup(self):
        '''
        setup browser
        '''
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory": "/Users/korouf/Desktop/TEXAS"}
        chromeOptions.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(executable_path='/Users/korouf/Documents/TexasScrape/TexasScrape/files/chromedriver',
                                   options=chromeOptions)  # fake Chrome browser mac
        # browser = webdriver.Chrome('C:\\Users\Frozm\PycharmProjects\\biologyScrapeData\\files\win\chromedriver.exe')
        return browser

    def open_second_page(self, url):
        browser = self.browser_setup()
        browser.get(url)
        try:  # docSearchButton
            leaseID = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="lease_numberTEXT"]')))
            leaseID.send_keys("38582")
            search = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="docSearchButton"]')))
            search.click()
            #searchResultsPageSize //*[@id="selectSize"]
            # selectmaximumresults = WebDriverWait(browser, 30).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[@id='searchResultsPageSize']")))
            time.sleep(6)

            selection = Select(browser.find_element_by_xpath('//*[@id="selectSize"]'))
            selection.select_by_value('50')
            tableid = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="searchResults"]')))
            # // *[ @ id = "searchResults"] / tbody / tr[4] / td[10]
            #result_list = tableid.find_elements(By.TAG_NAME,'tr')
            for rows in tableid.find_elements(By.TAG_NAME, 'tr'):
                for row in rows.find_elements(By.TAG_NAME, 'td'):
                    print(row.is_selected())

            #print(result_list)
            # element = WebDriverWait(browser, 30).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "//*[@id='searchResults']/tbody//td[contains(text(), 'POTENTIAL')]"))
            # )
            WebDriverWait(browser, 30)
            #print(element)
            input()
        except Exception as error:
            print(str(error))
