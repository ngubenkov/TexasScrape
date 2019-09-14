from selenium import webdriver
import stage3
import stage2
import stage4
DEFAULT_DOWNLOAD_DIRECTORY='/Users/frozmannik/PycharmProjects/TexasScrape/pdf'



def browser_setup(download_path):
    '''
    setup browser
    '''
    options = webdriver.ChromeOptions()

    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],  # Disable Chrome's PDF Viewer
               "download.default_directory": download_path, "download.extensions_to_open": "applications/pdf"}
    options.add_experimental_option("prefs", profile)
    browser = webdriver.Chrome('files/chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.
    return browser


if __name__ == '__main__':
    # open_page('MARTIN', '37 T2N', '36')
    browser = browser_setup(DEFAULT_DOWNLOAD_DIRECTORY)
    first_page = stage2.Stage2('MARTIN', '37 T2N', '36', browser)

    leaseIDs = first_page.open_page()
    print(first_page.leaseIDs)
    print(leaseIDs)
    for id in leaseIDs:
        second_page = stage3.OpenSecondPage(id)
        second_page.open_second_page(browser)
        third_page = stage4.Stage4(browser, id)
        third_page.stage4()
    #step_4("http://webapps.rrc.texas.gov/CMPL/publicSearchAction.do?formData.methodHndlr.inputValue =init&formData.headerTabSelected=home&formData.pageForwardHndlr.inputValue=home")
    #OpenSecondPage().open_second_page("​https://rrcsearch3.neubus.com/esd3-rrc/index.php?profile=17")

