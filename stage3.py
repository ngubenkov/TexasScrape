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

            browser = webdriver.Chrome(executable_path='/Users/korouf/Documents/TexasScrape/TexasScrape/files/chromedriver',
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
            #searchResultsPageSize //*[@id="selectSize"]
            # selectmaximumresults = WebDriverWait(browser, 30).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[@id='searchResultsPageSize']")))
            time.sleep(6)

            selection = Select(browser.find_element_by_xpath('//*[@id="selectSize"]'))
            selection.select_by_value('50')
            tableid = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="searchResults"]')))
            tbody = tableid.find_element_by_tag_name('tbody')
            # // *[ @ id = "searchResults"] / tbody / tr[4] / td[10]
            result_list = tableid.find_elements(By.TAG_NAME,'tr')
            for index1, rows in enumerate(tbody.find_elements(By.TAG_NAME, 'tr')):
                #col = rows.find_elements(By.TAG_NAME, 'td')
                for index2 , row in enumerate(rows.find_elements(By.TAG_NAME, 'td')):
                #print(col)
                #if col.get_attribute('headers') == 'thprofile_type':
                    if row:
                #     print(col[1])
                # print((index1,index2))
                        print(row)
                        col = tbody.find_elements(By.XPATH('//*[@id="searchResults"]/tbody/tr['+str(index1)+']/td['+str(index2)+']'))
                        print(col)
                #print(row.get_attribute('innerHtml'))
            # soup = BS(tableid,'html.parser')
            # right_rows = [tr.findAll('td') for tr in soup.findAll('tr')[:-1]]
            # r = []
            #
            # for i in right_rows:
            #     r.append([i[0].text])
            # print(r)
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
            browser.quit()

test = OpenSecondPage()
test.open_second_page("https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")