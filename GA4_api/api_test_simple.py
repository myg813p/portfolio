import pandas as pd
import os
from urllib import parse
import time

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
import urllib.parse

import requests
import warnings
from bs4 import BeautifulSoup as bs

import getpass
path_input = getpass.getuser()

# Ignore the InsecureRequestWarning message
warnings.filterwarnings(
    "ignore", message="Unverified HTTPS request is being made.")

# 한달간 날짜 코드 필요
# 네이버 애널리틱스 api 연결 필요
DIMENSIONS = "customEvent:IP_info_GA4"
DIMENSIONS = "customEvent:E_ttttttttttttttt"
DIMENSIONS = "linkDomain"
DIMENSIONS = "linkUrl"
DIMENSIONS = "pageReferrer"
DIMENSIONS = "sessionSource"
DIMENSIONS = "linkText"
DIMENSIONS = "fullPageUrl"


# Set up global variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'ga4python-373007-06ebe0e5ef57.json'


PROPERTY_ID = "347532431"
EXPORT_PATH = "export.csv"
DIMENSIONS = "eventName"
# METRICS = "activeUsers"
METRICS = "eventCount"
START_DATE = "2023-06-16"
END_DATE = "2023-06-18"
# END_DATE = "today"


# 네이버 웹 '동서가구' 검색 광고 트래픽 html
def get_naver_top(output):
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=동서가구'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    # print(output[0])

    body = soup.find('div', class_='brand_wrap')
    hrefs = body.find_all('a')
    all_cnt = 0
    list_item_cnt = 0
    before_ck_href = 'first'
    first_cnt = True
    for lk in hrefs:
        url = lk['href']
        res = requests.get(url, verify=False)
        lk['href'] = res.url

        ck_href = res.url.replace(
            "https://", "").split("&n_query=")[0] + '&n_query=동서가구'

        # count 확인 from test.html
        cnt = 0
        for lst in output:
            if lst[0].count(ck_href) > 0:
                cnt += int(lst[1])

        # 중복URL 더하지 않음
        if before_ck_href != ck_href:
            all_cnt += cnt
        # 첫번째 주소와 동일건은 중복 text 입력
        elif (first_cnt == False) and (first_ck_href == ck_href):
            cnt = f"{cnt}중복"
        print(ck_href)
        print(cnt)
        # 직전 주소 save
        before_ck_href = ck_href

        # 첫번째 주소 save
        if first_cnt == True:
            first_ck_href = ck_href
            first_cnt = False

        try:
            class_name = lk['class'][0]
        except:
            class_name = 'txt'

        if class_name == "direct_link":
            direct_link_text = soup.find("span", class_="direct_link_text")
            span_tag = soup.new_tag('span')
            span_tag.string = f'({str(cnt)})'
            span_tag['style'] = 'font-size:12px;color:red;'
            direct_link_text.insert_after(span_tag)

        elif class_name == 'link' or class_name == 'tit':
            lk.string = str(lk.string) + f'({str(cnt)})'
            lk['style'] = 'font-size:12px;color:red;'

        elif class_name == 'txt':
            txt = soup.find_all('div', class_='txt')
            txt[list_item_cnt].string = str(txt[list_item_cnt].string) + f'({str(cnt)})'
            txt[list_item_cnt]['style'] = 'font-size:12px;color:red;'
            list_item_cnt += 1

    # ALL_cnt
    print(all_cnt)
    all_cnt_show = soup.find("div", class_="direct_link_area")
    span_tag = soup.new_tag('p')
    span_tag.string = f'ALL ({str(all_cnt)})'
    span_tag['style'] = 'font-size:12px;color:red;'
    all_cnt_show.insert_before(span_tag)
    br = soup.new_tag('br')
    all_cnt_show.insert_before(br)

    # print(str(body))

    body = str(soup.find('div', class_='brand_wrap')
               ).replace('<em>', '<br><em>')

    elems = soup.find_all('link')
    css = ''
    for el in elems:
        if el['href'].count('main.c65ac745.css') or el['href'].count('search1_230216.css'):
            css += str(el)

    html = f'{css}{body}'

    # save as html
    with open("naver.html", 'w', newline='', encoding='utf-8-sig') as f:
        f.write(html)

# 네이버 모바일 '동서가구' 검색 광고 트래픽 html


def get_m_naver_top(output):
    url = 'https://m.search.naver.com/search.naver?query=동서가구'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')

    body = soup.find('section', class_='sc sp_brand ad_light_mode')
    # print(body)

    hrefs = body.find_all('a')
    print(len(hrefs))

    list_item_cnt = 0
    all_cnt = 0
    before_ck_href = 'first'
    for lk in hrefs:
        url = lk['href']
        res = requests.get(url, verify=False)
        lk['href'] = res.url

        ck_href = res.url.replace(
            "https://www", "m").split("&n_query=")[0] + '&n_query=동서가구'

        # count 확인 from test.html
        cnt = 0
        for lst in output:
            if lst[0].count(ck_href) > 0:
                cnt += int(lst[1])

        # 중복URL 더하지 않음
        if before_ck_href != ck_href:
            all_cnt += cnt
        # 직전 주소와 동일건은 중복 text 입력
        else:
            cnt = f"{cnt}중복"
        print(ck_href)
        print(cnt)
        # 직전 주소 save
        before_ck_href = ck_href

        parent_tag = lk.parent.get('class')[0]
        print(parent_tag)

        if  parent_tag == 'direct_link_area':
            direct_link_text = soup.find("a", class_="direct_link")
            span_tag = soup.new_tag('span')
            span_tag.string = f'({str(cnt)})'
            span_tag['style'] = 'font-size:12px;color:red;'
            direct_link_text.insert_after(span_tag)

        elif parent_tag =='thumb_area':
            p_tag = soup.new_tag('p')
            p_tag.string = f'({str(cnt)})'
            p_tag['style'] = 'font-size:12px;color:red;'
            lk.insert_after(p_tag)

        elif parent_tag =='subtit' or parent_tag =='tit' or parent_tag =='desc':
            lk.string = str(lk.string) + f'({str(cnt)})'
            lk['style'] = 'font-size:15px;color:red;'

        elif parent_tag == 'list_item':
            txt = soup.find_all('div', class_='txt')
            txt[list_item_cnt].string = str(txt[list_item_cnt].string) + f'({str(cnt)})'
            txt[list_item_cnt]['style'] = 'font-size:14px;color:red;'
            list_item_cnt += 1

        elif parent_tag == 'btn':
            lk.string = str(lk.string) + f'({str(cnt)})'
            lk['style'] = 'font-size:14px;color:red;'

    all_cnt_show = soup.find('div', class_="direct_link_area")
    div_tag = soup.new_tag('div')
    div_tag.string = f'ALL ({str(all_cnt)})'
    div_tag['style'] = 'font-size:12px;color:red;'
    all_cnt_show.insert_before(div_tag)
    print('all_cnt', all_cnt)

    # css
    elems = soup.find_all('link')
    css = ''
    for el in elems:
        if el['href'].count('main.9ae0126b.css') or el['href'].count('w_new_230309.css'):
            css += str(el)

    html = f'{css}{body}'
    # save as html
    with open("naver_m.html", 'w', newline='', encoding='utf-8-sig') as f:
        f.write(html)

# 네이버 '동서가구' 검색 광고 트래픽 cnt


def naver_cnt(property_id, export_path, dimensions, start_date, end_date, metrics):
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="fullPageUrl")],
        metrics=[Metric(name=metrics)],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)

    output = []
    print("Report result(naver):")
    for row in response.rows:
        try:
            decoded1 = urllib.parse.unquote(row.dimension_values[0].value)
            temp = [decoded1, row.metric_values[0].value]
            output.append(temp)
        except:
            pass
    get_m_naver_top(output)
    get_naver_top(output)

# 동서가구 자사몰 cnt


def sample_run_report(property_id, export_path, dimensions, start_date, end_date, metrics):
    """Runs a simple report on a Google Analytics 4 property."""

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=dimensions)],
        metrics=[Metric(name=metrics)],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)

    output = []
    print("Report result:")
    for row in response.rows:
        # print(row.dimension_values[0].value, row.metric_values[0].value)
        output.append(
            # {dimensions: row.dimension_values[0].value, "VALUE": row.metric_values[0].value})
            [parse.unquote(row.dimension_values[0].value),
             row.metric_values[0].value]
        )
    df = pd.DataFrame(output)
    # df.to_csv(f'{export_path}_{start_date}~{end_date}.csv', encoding="utf-8-sig")
    print(len(output))
    df.to_csv(f'test.html', encoding="utf-8-sig")

# 파일 저장


def web_ftp():
    from bs4 import BeautifulSoup as bs
    import os
    import time
    import urllib3
    import datetime

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

    # 옵션 - 셀레니움
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink_features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable_logging"])
    options.add_argument("no_sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extionsions")
    options.add_experimental_option("useAutomationExtension", False)
    # options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)

    # 고도몰 로그인
    url = 'http://gdadmin.edftr76860385.godomall.com/base/login.php'
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element(By.NAME, 'managerId').send_keys('dfgagu')
    time.sleep(0.5)
    driver.find_element(By.NAME, 'managerPw').send_keys('df1051184@!')
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, 'btn.btn-black').click()

    # web_ftp 페이지
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "menu_order")))
    url = 'http://gdadmin.edftr76860385.godomall.com/share/popup_webftp.php?dir=data/0cp'
    driver.get(url)
    driver.implicitly_wait(5)

    data = ['test.html', 'click.js', 'naver.html', 'naver_m.html']
    upload_cnt = 0
    while True:
        for file in data:
            ads = f'C:/Users/{path_input}/OneDrive/바탕 화면/code/0000/{file}'
            print(ads)
            driver.find_element(By.ID, "filer").send_keys(r""+ads)
            time.sleep(1.5)

            # 첫번째 경고창
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

        if (date[:16] == now[:16]) or upload_cnt > 1:
            break
        else:
            upload_cnt += 1
            print('전송실패 다시시도')

    print(f'업로드일 : {date}')
    print(f'현재시간 : {now[:19]}')
    driver.quit()
    print('전송완료')


# main
# main
# main
# main
naver_cnt(PROPERTY_ID, EXPORT_PATH, DIMENSIONS, START_DATE, END_DATE, METRICS)
sample_run_report(PROPERTY_ID, EXPORT_PATH, DIMENSIONS, START_DATE, END_DATE, METRICS)
time.sleep(1)
web_ftp()
