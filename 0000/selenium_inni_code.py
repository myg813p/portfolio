import os
import urllib3
import getpass
path_input = getpass.getuser()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import chromedriver_autoinstaller
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'C:/Users/{path_input}/AppData/Local/Programs/Python/Python310\{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chrome driver is installed: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
chromedriver_autoinstaller.install(True)


#옵션 - 셀레니움
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink_features=AutomationControlled")
options.add_experimental_option("excludeSwitches",["enable_logging"])
options.add_argument("no_sandbox")
options.add_argument("--start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extionsions")
options.add_experimental_option("useAutomationExtension",False)
#options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")
driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)
