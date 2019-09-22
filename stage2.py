from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyscreenshot as ImageGrab
from tableScrape import scrapeTable
import time
from selenium.webdriver.common.action_chains import ActionChains
import os

waiting = 1


class Stage2:
    def __init__(self, country, block, section, browser):
        self.country = country
        self.block = block
        self.section = section
        self.leaseIDs = set()
        self.browser = browser
        self.mainFolder = self.country + "_" + self.block + "_" + self.section
        self.wells = []

    def open_page(self):
        '''
        open browser and click
        '''
        url = "http://gis.rrc.texas.gov/gisviewer/"
        self.browser.get(url)
        try:
            #self.createFolder()
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="rrcsearchButton"]'))).click()
            time.sleep(waiting)
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="dijit_rrcGisAnchorMenuItem_7_text"]'))).click()
            time.sleep(waiting)
            self.inputData(self.browser)

            e = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="rrcGisViewerMap_graphics_layer"]')))
            time.sleep(waiting)
            # identify wells
            WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '// *[ @ id = "identifyButton"] / span[1]'))).click()
            WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '// *[ @ id = "dijit_rrcGisAnchorMenuItem_0_text"]'))).click()

        except Exception as e:
            print(str(e))

        self.testHover(self.browser)
        return self.leaseIDs if self.leaseIDs else None

    def createFolder(self):
        '''
        create folder for project
        '''
        if not os.path.exists(self.mainFolder):
            os.makedirs(self.mainFolder)

    def inputData(self, browser):
        '''
        input data in search
        '''
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="countySelect"]/tbody/tr/td[2]/div[1]'))).click()  # select countries btn
        items = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'dijitMenuItemLabel')))  # list of drop down items

        for _ in items:
            if self.country.upper() in _.get_attribute('innerHTML'):
                _.click()

        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "blockID"]'))).send_keys(self.block)  # Block
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "sectionID"]'))).send_keys(self.section)  # Section
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '// *[ @ id = "querySurveyButton_label"]'))).click()  # Query button
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#fpSurveySearch #zoomCloseBtn a img'))).click()  # close form
        time.sleep(5)
        self.screenshot()  # dont use it now

        # get coordinates of wells inside of area by hover them and and if pop up isn't appear save coordinates
        self.get_wells(browser)

    def get_wells(self, browser):
        wellMap = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rrcGisViewerMap"]')))
        wellimages = wellMap.find_elements_by_tag_name('image')
        wells = 0

        for image in wellimages:
            try:
                hover = ActionChains(browser).move_to_element(image)
                hover.perform()
                time.sleep(1)
                descriptionForm = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'dijitTooltipContainer')))
                br = descriptionForm.find_element(By.CLASS_NAME, "dijitTooltipFocusNode")
                if '"{}"'.format(self.section) in br.text[br.text.find('Lease Name :'):br.text.find('On Schedule :')]:
                    print("FOUND ")

                    image.click()
                    time.sleep(3)
                    self.scrapePopUp(browser, image)

            except:
                print("Potensial correct")
                wells += 1
                self.wells.append(image)

                pass
        print("TOTAL WELLS {}".format(wells))

    def screenshot(self):
        im = ImageGrab.grab()
        if os.path.exists(self.mainFolder + '/screenshots'):
            im.save(self.mainFolder + '/screenshots/{}_{}_{}.png'.format(self.country, self.block, self.section))
        else:
            os.makedirs(self.mainFolder + '/screenshots')
            im.save(self.mainFolder + '/screenshots/{}_{}_{}.png'.format(self.country, self.block, self.section))

    def testHover(self, browser):
        wells = 0
        for image in self.wells:
            try:
                hover = ActionChains(browser).move_to_element(image)
                hover.perform()
                time.sleep(1)
                descriptionForm = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'dijitTooltipContainer')))
                br = descriptionForm.find_element(By.CLASS_NAME, "dijitTooltipFocusNode")
                if br:
                    print("FOUND ")
                    wells += 1
                    image.click()
                    time.sleep(3)
                    self.scrapePopUp(browser, image)

            except:
                print(" Acceptable shit happened")
                pass
        print("TOTAL WELLS {}".format(wells))

    def hoverBtns(self, browser):
        '''
        go throw all well on the map
        hover each btn
        :param browser:
        :return:
        '''
        wellMap = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rrcGisViewerMap"]')))
        wellimages = wellMap.find_elements_by_tag_name('image')
        wells = 0

        for image in wellimages:
            try:
                hover = ActionChains(browser).move_to_element(image)
                hover.perform()
                time.sleep(1)
                descriptionForm = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'dijitTooltipContainer')))
                br = descriptionForm.find_element(By.CLASS_NAME, "dijitTooltipFocusNode")
                if '"{}"'.format(self.section) in br.text[br.text.find('Lease Name :'):br.text.find('On Schedule :')]:
                    print("FOUND ")
                    wells += 1
                    image.click()
                    time.sleep(3)
                    self.scrapePopUp(browser, image)

            except:
                print(" Acceptable shit happened")
                pass
        print("TOTAL WELLS {}".format(wells))

    def scrapePopUp(self, browser, image):
        tbodys = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'esriPopupWrapper'))).find_elements_by_tag_name('tbody')
        print("FOUND POP UP ")
        count = 0
        tempL, tempR = None,None
        for item in tbodys:
            count += 1
            try:
                tableContent = item.get_attribute('innerHTML')
                if count==1:
                    tempL,tempR = scrapeTable(tableContent, self.mainFolder)
                else:
                    id = scrapeTable(tableContent, self.mainFolder,tempL,tempR)
                    self.leaseIDs.add(id)
                print("TABLE SCRAPED SUCCESSFULLY {}".format(count))

            except Exception as e:
                print("NON ACCEPTABLE SHIT HAPPENED CANT SCRAPE Table {} exception : {}".format(count, str(e)))

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
