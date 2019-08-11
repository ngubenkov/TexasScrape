from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as BS
import pyscreenshot as ImageGrab

class OpenSecondPage:
    def browser_setup(self):
        '''
        setup browser
        '''
        try:
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"download.default_directory": "/Users/korouf/Desktop/TEXAS"}
            chromeOptions.add_experimental_option("prefs", prefs)

            browser = webdriver.Chrome(executable_path='files/chromedriver',
                                       options=chromeOptions)  # fake Chrome browser mac
            #browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
            return browser
        except Exception as e:
            print(str(e))


    def open_second_page(self, url):
        browser = self.browser_setup()
        try:
            browser.get(url)
        except Exception as err:
            print(str(err))
        try:  # docSearchButton
            leaseID = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="lease_numberTEXT"]')))
            leaseID.send_keys("38582")
            search = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="docSearchButton"]')))
            search.click()

            time.sleep(6)

            selection = Select(browser.find_element_by_xpath('//*[@id="selectSize"]'))
            # select possibly all result if no other page
            selection.select_by_value('50')
            # get table
            tableid = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="searchResults"]')))
            tbody = tableid.find_element_by_tag_name('tbody') # get the body of the table
            result_list = tbody.find_elements(By.TAG_NAME, 'tr') # get all the tr of the table above
            for index1, rows in enumerate(result_list):
                col = rows.find_elements(By.TAG_NAME, 'td')
                for index2, row in enumerate(col):
                    if row and row.get_attribute('headers') == 'thprofile_type' and \
                            row.get_attribute('innerHTML') == 'POTENTIAL':
                        print (tbody.get_attribute('innerHTML'))
                        print(tbody.get_attribute('@data-docid'))
                        print(tableid.find_elements(By.XPATH, '//*[@data-docid]')[0].get_attribute('innerHTML'))

            WebDriverWait(browser, 30)
            #print(element)
            input()
        except Exception as error:
            print(str(error))
            browser.quit()




if __name__ == '__main__':
    test = OpenSecondPage()
    test.open_second_page("https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")


    '//*[@id="STANDARD_Zc4AGPmrB0s."]'
    '//*[@id="STANDARD_SDlGy2DN744."]'