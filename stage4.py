from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyscreenshot as ImageGrab
from tableScrape import scrapeTable


class Stage4:
    def __init__(self, browser, id):
        self.browser = browser
        self.id = id

    def screenshot(self):
        im = ImageGrab.grab()
        im.save('screenshots/leaseID_{}.png'.format(str(self.id)))
        im.show()

    def stage4(self):
        try:
            self.browser.get('http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home')
        except:
            self.browser.get( 'http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home')
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="leaseNoArgHndlr:12"]'))).send_keys(self.id)  # Block
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[6]/tbody/tr/td/form/table/tbody/tr[4]/td/table/tbody/tr[5]/td/table/tbody/tr/td/input[1]'))).click()
        #screenshot(self.id)
        recordsFoundLinks = scrapeTable(self.browser)
        for record in recordsFoundLinks:
            details = self.scrapeDetails(record)
            for detail in details:
                self.browser.get(detail[1])
            print("click to go to next detail")


    def scrapeTable(self):
        table = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[6]/tbody/tr/td/form/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody')))
        links = table.find_elements_by_tag_name('a')
        returnList = []

        for i in links[12:]:
            returnList.append(i.get_attribute("href"))

        return returnList

    def scrapeDetails(self, url):
        self.browser.get(url)
        table = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[6]/tbody/tr/td/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody')))
        rows = table.find_elements_by_tag_name('tr')
        attachments = []

        for row in rows[1:]:
            try:
                url = row.find_element_by_tag_name('a').get_attribute('href')
                name = row.find_element_by_tag_name('td').find_element_by_tag_name('div').get_attribute('innerHTML')
                attachments.append([name, url])
            except:
                pass

        return attachments


