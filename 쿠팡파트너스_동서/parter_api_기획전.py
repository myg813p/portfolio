url_code = False
ftp_code = False

import time
import re
import html
from bs4 import BeautifulSoup
import requests
import csv

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

def web_ftp():

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

def short_url(link):
    import hmac
    import hashlib
    import json
    from time import gmtime, strftime
    import time

    REQUEST_METHOD = "POST"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    # KEY
    ACCESS_KEY = 'd41d0ed7-3c53-4ca0-83db-e1bb585e268e'         #동서가구 A_Key
    SECRET_KEY = '11588f33eda8c03ebd714af7542c68eafd2731df'     #동서가구 S_Key

    def generateHmac(method, url, secretKey, accessKey):
        path, *query = url.split("?")
        datetimeGMT = strftime('%y%m%d', gmtime()) + \
            'T' + strftime('%H%M%S', gmtime()) + 'Z'
        message = datetimeGMT + method + path + (query[0] if query else "")

        signature = hmac.new(bytes(secretKey, "utf-8"),
                             message.encode("utf-8"),
                             hashlib.sha256).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)

    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)

    items = [link]

    for item in items:
        REQUEST = {"coupangUrls": [item]}
        response = requests.request(method=REQUEST_METHOD, url=url,
                                    headers={
                                        "Authorization": authorization,
                                        "Content-Type": "application/json"
                                    },
                                    data=json.dumps(REQUEST)
                                    )
        c_deeplink = response.json()
        # 딥링크 변환 안되는 상품 구별을 위해 rCode를 가지고 옴
        r_code = c_deeplink['rCode']

        if r_code == '0':   # 정상 코드 '0'
            c_data = c_deeplink['data']
            # 쿠팡에서 받는 API는 배열, 딕셔너리 이중구조라서 먼저 배열에서 값을 추출
            convert_data = c_data[0]
            convert_url = convert_data['shortenUrl']    # 딕셔너리에서 shortenUrl만 추출
        else:
            # 딥링크 변환 불가 코드: 400204
            # convert_url = 'no shortenUrl....... error code : ' + r_code
            convert_url = '없음'

        # print(convert_url)
        return convert_url


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
}


# title글자수
def len_words(test):
    temp = re.compile('[가-힣]+').findall(test)
    test1 = ''
    for i in temp:
        test1 = test1+i
    test2 = re.compile('[가-힣]+').sub('', test)
    return len(test1)*2+len(test2)


##
url = 'https://pages.coupang.com/p/79202?from=home_C1&traid=home_C1&trcid=11223227'

url = 'https://pages.coupang.com/p/81848?src=1139000&spec=10799999&addtag=600&ctag=81848&lptag=AF1723348&itime=20230201153353&pageType=EVENTPAGE&pageValue=81848&wPcid=16532709741816198565144&wRef=&wTime=20230201153353&redirect=landing&traceid=V0-181-0000000000000000&subid=&subparam='

url = 'https://pages.coupang.com/p/81848?src=1139000&spec=10799999'


driver.get(url)
driver.implicitly_wait(5)
time.sleep(5)
htmll = driver.page_source

# res = requests.get(url, verify=False, headers=headers)
# htmll = html.unescape(res.text)


soup = BeautifulSoup(htmll, 'html.parser')

parts = soup.find_all('div', class_='part')
#print(len(parts))

all_list = []
cnt = 0
MAX = 0
for part in parts:
    elems = part.find_all('li', class_='recommend-widget__item c-product')
    #print(elems[0])

    if len(elems) >= 5:
        here = 20
    elif len(elems) == 4:
        here = len(elems)
    else:
        here = 0

    #print(here)
    if here > 0:
        for i in range(here):
            try:
                # 0링크
                link = (elems[i].find('a')['href']).replace('https://www.','https://m.').replace('/vp/', '/vm/').replace('&isAddedCart=', '')
                if url_code == True:
                    link = short_url(link)

                if link.count('없음') == 0:
                    #
                    temp_list = []

                    # 1상품 이미지
                    img = elems[i].find('div', class_='recommend-widget__item__image-wrap')
                    #print('img', img)
                    try:
                        thumbnail = 'https:' + elems[i].find('img')['src']
                    except:
                        thumbnail = 'https:' + elems[i].find('img')['lazy-load']
                        print('lazy')
                    #print(thumbnail)

                    # 2상품명
                    title = elems[i].find('strong', class_='recommend-widget__item__title').text.replace('\n', '').replace('\t', '').replace('\r', '').strip()
                    title_cnt = len_words(title)
                    if title_cnt <= 27:
                        title = title + ' ' + price + '원'
                    elif title_cnt > 43:
                        title = title[:23]
                    #print(title)

                    # 3할인율 (옵)
                    try:
                        discount_percentage = elems[i].find('span', class_='discount-percentage').text.strip()
                    except:
                        discount_percentage = 'none'
                    #print(discount_percentage)

                    # 4할인전 가격 (옵)
                    try:
                        base_price = elems[i].find('del', class_='base-price').text.strip()
                    except:
                        base_price = 'none'
                    #print(base_price)

                    # 5판매가
                    price = elems[i].find('strong', class_='price-value').text
                    #print(price)




                    # 6로켓 로고 (옵)
                    # //image10.coupangcdn.com/image/delivery_badge/default/ios/rocket_merchant/consignment_v3@2x.png
                    # 제트배송
                    # //image6.coupangcdn.com/image/cmg/icon/ios/logo_rocket_large@3x.png
                    # 로켓배송
                    # //image6.coupangcdn.com/image/badges/falcon/v1/web/rocket-fresh@2x.png
                    # 로켓프레시
                    try:
                        descriptions = elems[i].find('span', class_='badge rocket')
                        rocket = 'https:'+descriptions.find('img')['src']
                        if rocket.count('rocket') == 0 and rocket.count('consignment') == 0:
                            rocket = 'none'
                    except:
                        rocket = 'none'
                    #print(rocket)

                    # 7별수 (옵)
                    try:
                        rating_star = elems[i].find('div', class_='rating-star').text[:4].strip()
                    except:
                        rating_star = 'none'
                    

                    # 8리뷰수 (옵)
                    try:
                        rating_total_count = elems[i].find('span', class_='rating-total-count').text.replace('(','').replace(')','').strip()
                    except:
                        rating_total_count = 'none'
                    
                    print(link)
                    print(thumbnail)
                    print(title)
                    print(discount_percentage)
                    print(base_price)
                    print(price)
                    print(rocket)
                    print(rating_star)
                    print(rating_total_count)

                    temp_list.append(link)
                    temp_list.append(thumbnail)
                    temp_list.append(title)
                    temp_list.append(discount_percentage)
                    temp_list.append(base_price)
                    temp_list.append(price)
                    temp_list.append(rocket)
                    temp_list.append(rating_star)
                    temp_list.append(rating_total_count)
                    
                    all_list.append(temp_list)

                    MAX += 1
                    print(f'{MAX+1}/{len(elems)}')
                if MAX >= 95:
                    break
            except:
                pass
        if MAX >= 95:
            print(f'상품 {cnt} 건 수집완료')
            break

list_to_html = str(all_list)
list_to_html = list_to_html.replace('[[','').replace(']]','')
list_to_html = list_to_html.replace('[','').replace('],',',,')
list_to_html = list_to_html.replace("',",',,')
list_to_html = list_to_html.replace("'",'')


#html 저장
with open("list_html.html", 'w', newline='', encoding='utf-8-sig') as f:
    f.write(list_to_html)
print('저장')

if ftp_code == True:
    web_ftp()