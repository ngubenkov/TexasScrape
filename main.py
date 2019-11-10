from selenium import webdriver
import upload_files
import stage3
import stage2
import stage4
import os
import sys
package_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOWNLOAD_DIRECTORY='~/TexasScrape/pdf'

def browser_setup(download_path):
    '''
    setup browser
    '''
    options = webdriver.ChromeOptions()

    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],  # Disable Chrome's PDF Viewer
               "download.default_directory": download_path, "download.extensions_to_open": "applications/pdf"}
    options.add_experimental_option("prefs", profile)
    browser = webdriver.Chrome(package_dir+'\\files\\chromedriver.exe',chrome_options=options)  # Optional argument, if not specified will search path.
    return browser


if __name__ == '__main__':
    print(package_dir)
    arguments = sys.argv[1:]
    for index, arg in enumerate(arguments):
        arguments[index] = arg.replace(',', ' ')
    main_folder = '_'.join(arguments)

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    browser = browser_setup(main_folder)
    first_page = stage2.Stage2(arguments[0], arguments[1], arguments[2], browser)

    leaseIDs = first_page.open_page()
    for id in leaseIDs:
        second_page = stage3.OpenSecondPage(id)
        second_page.open_second_page(browser)
        third_page = stage4.Stage4(browser, id)
        third_page.stage4()
    upload_files.upload_allfiles_google(main_folder)