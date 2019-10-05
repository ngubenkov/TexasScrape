from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, Chrome
import time
import os

DEFAULT_DOWNLOAD_DIRECTORY = '/Users/korouf/Desktop/TEXAS'


class OpenSecondPage:
    def __init__(self, key):
        self.key = key
        self.createFolder()

    def createFolder(self):
        if os.path.exists(self.key) == False:
            os.makedirs("pdf/"+self.key)

    # TODO: Find a way to change default downloading folder of already existing browser
    def changeBrowserSettings(self):
        options = ChromeOptions()
        profile = { "plugins.plugins_disabled" : "Chrome PDF Viewer",  # Disable Chrome's PDF Viewer
                    "download.default_directory": '/Users/frozmannik/PycharmProjects/TexasScrape/pdf/'+self.key,
                    "plugins.always_open_pdf_externally": True,
                    "download.extensions_to_open": "applications/pdf/"+self.key}
        options.add_experimental_option("prefs", profile)
        browser = Chrome('files/chromedriver', chrome_options=options)
        return browser

    def checkDownload(self):
        print("HERE")
        print(os.listdir("pdf/{}".format(self.key)))


    def open_second_page(self, browser):
        try:
            browser.get("https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")
            self.createFolder()
            browser = self.changeBrowserSettings() # change browser settings( new downloading path)
            self.checkDownload()
        except Exception as err:
            print(str(err))
        try:  # docSearchButton
            leaseID = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="lease_numberTEXT"]')))
            leaseID.send_keys(self.key)
            search = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="docSearchButton"]')))
            search.click()

            time.sleep(6)

            selection = Select(browser.find_element_by_xpath('//*[@id="selectSize"]'))
            # select possibly all result if no other page
            selection.select_by_value('50')
            # get table
            time.sleep(5)
            tableid = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="searchResults"]')))
            tbody = tableid.find_element_by_tag_name('tbody') # get the body of the table
            result_list = tbody.find_elements(By.TAG_NAME, 'tr') # get all the tr of the table above
            download_ids = []
            for index1, rows in enumerate(result_list):
                col = rows.find_elements(By.TAG_NAME, 'td')
                for index2, row in enumerate(col):
                    if row and row.get_attribute('headers') == 'thprofile_type' and \
                            row.get_attribute('innerHTML') == 'POTENTIAL':
                        # get the correct id
                        docid = tableid.find_elements(By.XPATH, '//*[@data-docid]')[index1].get_attribute("data-docid")
                        downloadid = 'STANDARD_'+str(docid)
                        download_ids.append(downloadid)
                        action_menu_lst = result_list[index1].find_element(By.CLASS_NAME, 'showActionMenu')
                        # click to open menu
                        action_menu_lst.click()
                        time.sleep(4)
                        # get  to the download page
                        WebDriverWait(browser, 30).until(
                            EC.presence_of_element_located((By.ID, downloadid))).click()
                        download_button = WebDriverWait(browser, 30).until(
                            EC.presence_of_element_located((By.ID, 'downloadMenuButton'))).click()
                        time.sleep(3)
                        WebDriverWait(browser, 30).until(
                            EC.presence_of_element_located((By.ID, 'downloadAllButton'))).click()
                        time.sleep(2)

                        self.checkDownload() # check if file downloading
                        browser.switch_to.window(browser.window_handles[1])
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        WebDriverWait(browser, 30).until(
                            EC.presence_of_element_located((By.ID, 'closeDoc2'))).click()
                        time.sleep(2)

            print(download_ids)
            WebDriverWait(browser, 30)
        except Exception as error:
            print(str(error))
            browser.quit()

# test = OpenSecondPage(38582)
# test.open_second_page()