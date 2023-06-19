def web_ftp():
    from bs4 import BeautifulSoup as bs
    import os
    import time
    import urllib3
    import datetime


    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    input_main1 = 'DSF20220704001'
    input_main2 = 'data2'
    input1 = 'sub_1'
    input2 = 'sub_2'
    input3 = 'sub_3'
    input4 = 'sub_4'

    path_input = input_main1


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

    #고도몰 로그인
    url = 'http://gdadmin.edftr76860385.godomall.com/base/login.php'
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element(By.NAME,'managerId').send_keys('dfgagu')
    time.sleep(0.5)
    driver.find_element(By.NAME,'managerPw').send_keys('df1051184!@')
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, 'btn.btn-black').click()

    #web_ftp 페이지
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_order")))
    url = 'http://gdadmin.edftr76860385.godomall.com/share/popup_webftp.php?dir=data/0cp'
    driver.get(url)
    driver.implicitly_wait(5)


    data = ['list_html.html', 'list_css.css']
    upload_cnt = 0
    while True:
        for file in data:
            ads = f'C:/Users/{path_input}/OneDrive/바탕 화면/code/쿠팡파트너스_동서/{file}'
            print(ads)
            driver.find_element(By.ID, "filer").send_keys(r""+ads)
            time.sleep(1.5)

            #첫번째 경고창
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                # alert.dismiss()
                alert.accept()
            except:
                print("no alert")
            time.sleep(1)

        driver.get(url)
        time.sleep(1)
        date = driver.find_elements(By.CLASS_NAME, 'font-date')[1].text
        now = str(datetime.datetime.now())

        if (date[:16] == now[:16]) and upload_cnt > 0:
            break
        else:
            upload_cnt+=1
            print('전송실패 다시시도')

    print(f'업로드일 : {date}')
    print(f'현재시간 : {now[:19]}')
    print('전송완료')
