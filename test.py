from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option('excludeSwitches',['disable-sync']) 
options.add_argument('--enable-sync')
#options.add_argument("--disable-infobars")
options.add_argument("user-data-dir=/Users/irad/Library/Application Support/Google/Chrome/")
driver = webdriver.Chrome(options=options)

while True:
    sleep(5)
    print(driver)
