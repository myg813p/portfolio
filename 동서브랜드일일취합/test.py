from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import 상품리스트_동서식품
import 상품리스트_매일유업
import 상품리스트_KN디지털
import 상품리스트_결합상품
import 상품리스트_트라이스
import 상품리스트_파로마리빙

import time
import schedule

import csv
from bs4 import BeautifulSoup as bs

import getpass
path_input = getpass.getuser()

def main():
    import os
    import time
    import urllib3

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
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[
        0]
    driver_path = f'C:/Users/{path_input}/AppData/Local/Programs/Python/Python310\{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrome driver is installed: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

    # 옵션 - 셀레니움
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--disable-blink_features=AutomationControlled")
    options.add_experimental_option(
        "excludeSwitches", ["enable_logging"])
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

    def get(driver):
        import socket
        import re
        import requests
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("pwnbit.kr", 443))
        in_ip = sock.getsockname()[0]
        print("내부 IP: ", in_ip)

        req = requests.get("http://ipconfig.kr")
        ex_ip = re.search(
            r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
        print("외부 IP: ", ex_ip)

        if ex_ip != '121.133.167.1622':
            while_cnt = 0
            while True:
                # 고도몰 로그인
                url = 'http://gdadmin.edftr76860385.godomall.com/base/login.php'
                driver.get(url)
                driver.implicitly_wait(5)
                driver.find_element(By.NAME, 'managerId').send_keys('dfgagu')
                time.sleep(0.5)
                driver.find_element(By.NAME, 'managerPw').send_keys('df1051184@!')
                time.sleep(0.5)
                driver.find_element(By.CLASS_NAME, 'btn.btn-black').click()

                # 공급사 선택
                elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "menu_order")))
                url = 'http://gdadmin.edftr76860385.godomall.com/order/order_list_all.php?view=orderGoods&'
                driver.get(url)
                driver.implicitly_wait(5)

                driver.find_element(
                    By.XPATH, '//*[@id="frmSearchOrder"]/div[2]/table/tbody[1]/tr[1]/td/input').click()
                time.sleep(0.5)

                elem = driver.find_elements(
                    By.CLASS_NAME, 'pagination.pagination-sm')[1]
                lis = elem.find_elements(By.TAG_NAME, 'li')

                url_add = 'http://gdadmin.edftr76860385.godomall.com/order/order_list_all.php?detailSearch=y&scmFl=1'
                for page in range(1, len(lis)+1):
                    if page != 1:
                        driver.find_element(
                            By.XPATH, f'//*[@id="layer-wrap"]/div[2]/nav/ul/li[{str(page)}]/a').click()
                        time.sleep(1)

                    table2 = driver.find_elements(
                        By.CLASS_NAME, 'table.table-rows')[1]
                    labels = table2.find_elements(By.TAG_NAME, 'label')
                    for label in labels:
                        if label.text.count('동서가구') == 0:
                            label_no = label.get_attribute('for')
                            label_no = '&scmNo[]=' + \
                                re.sub(r'[^0-9]', '', label_no)
                            label_temp = label.text
                            label_temp = label_no + '&scmNoNm[]=' + \
                                label_temp.replace(" ", "+")
                            url_add = url_add + label_temp

                if while_cnt == 0:
                    # setting url
                    now = datetime.now()
                    today = now.strftime("%Y-%m-%d")
                    month = now - relativedelta(months=6)
                    # month = now - relativedelta(day=7)

                    month_minus_one_day = month + timedelta(days=2)
                    month6 = month_minus_one_day.strftime("%Y-%m-%d")
                    data_EA = 10000

                print(today)
                print(month6)
                url_add = url_add + \
                    f'''&key[]=o.orderNo&keyword[]=&key[]=o.orderNo&keyword[]=&key[]=o.orderNo&keyword[]=&goodsKey=og.goodsNm&goodsNo=&goodsText=&treatDateFl=og.regDt&searchPeriod=0&treatDate[]={month6}&treatTime[]=00:00:00&treatDate[]={today}&treatTime[]=23:59:59&orderStatus[]=o1&orderStatus[]=p1&orderStatus[]=g1&orderStatus[]=d1&orderStatus[]=d2&orderStatus[]=s1&invoiceCompanySno=0&invoiceNoFl=&orderMemoCd=&memFl=&settlePrice[]=&settlePrice[]=&receiptFl=&overDepositDay=&underDeliveryDay=&sort=og.orderNo+desc&pageNum={data_EA}&view=orderGoods&searchFl=y&applyPath=/order/order_list_all.php?view=orderGoods'''

                # 동서가구 제외 브랜드 3개월치 검색
                driver.get(url_add)
                driver.implicitly_wait(10)
                try:
                    from selenium.webdriver.common.alert import Alert
                    # Switch to the alert
                    alert = Alert(driver)
                    # Get the text of the alert
                    alert_text = alert.text
                    # Print the alert text
                    print(alert_text)
                    if alert_text.count('6개월이상'):
                        import datetime as datetime2
                        date_object = datetime2.datetime.strptime(month6, '%Y-%m-%d')
                        new_date = date_object + datetime2.timedelta(days=1)
                        month6 = new_date.strftime('%Y-%m-%d')
                        alert.accept()
                        while_cnt+=1
                except:
                    break


            #html 들고오기
            htmll = driver.page_source

            soup_origin = bs(htmll, 'html.parser')
            soup = soup_origin.find('div', class_='table-responsive')

            # title 제어
            pass_title = ['교환', '환불', '반품']
            pass_state = ['중단', '환불', '실패', '취소', '반품']
            replace_words = ['무료배송', '의자BEST', '땡처리특가', '가격인하특가', 'MD추천', '무료배송 특가', '/낱개선택', '/무료배송','제주도배송','동서특가', '설연휴특가', '원데이특가', '원데이행사', '브랜드위크', '동서가구 단독/쿠폰다운', '주말특가', '주말 특가', '위클리딜', '식탁생활', '최저가 도전', '1% 추가할인', '사은품증정', '소파마켓', '[단독쿠폰(~4/30까지)]', 'BEST인기식탁', '[']

            # 자료
            lists = []
            lists_1 = []
            lists_2 = []

            tbody = soup.find('tbody')
            tr = tbody.find_all('tr', class_='text-center')

            for trs in tr:

                # 날짜
                date = trs.find('td', class_='font-date nowrap').text.strip()[:10]

                # 시간
                ttime = trs.find('td', class_='font-date nowrap').text.strip()[10:]

                # 주소
                url = trs.find('td', class_='text-left').find('a')['href']

                # 이미지
                img = trs.find('td', class_='text-left').find('img')['src']

                # 상품명
                title = trs.find(
                    'a', class_='one-line bold mgb5').text.replace('\n', '')

                # replace_word1
                title = title.replace("]", " ")

                while True:
                    title = title.replace('  ', ' ')
                    if title.count('  ') == 0:
                        break

                # replace_words2
                for rps in replace_words:
                    title = title.replace(rps, '')
                title = title.strip()

                # (주)안산동서물류	 상품리스트
                for items in 상품리스트_동서식품.itme_list:
                    if title.count(items) > 0:
                        title = '(주)안산동서물류 ' + title

                # 해담솔 상품리스트
                for items in 상품리스트_매일유업.itme_list:
                    if title.count(items) > 0:
                        title = '해담솔 ' + title

                # KN디지털 상품리스트
                for items in 상품리스트_KN디지털.itme_list:
                    if title.count(items) > 0:
                        title = 'KN디지털 ' + title

                # 결합상품 상품리스트
                for items in 상품리스트_결합상품.itme_list:
                    if title.count(items) > 0:
                        title = '결합상품 ' + title

                # 트라이스 상품리스트
                for items in 상품리스트_트라이스.itme_list:
                    if title.count(items) > 0:
                        title = '트라이스 ' + title

                # 파로마리빙 상품리스트
                for items in 상품리스트_파로마리빙.itme_list:
                    if title.count(items) > 0:
                        title = '파로마리빙 ' + title

                # 온우리가구 상품리스트
                if title.count('솔로리빙') > 0:
                    title = '온우리가구 ' + title

                # 주식회사 홍시 상품리스트
                if title.count('리브우드') + title.count('로티에') > 0:
                    title = '주식회사_홍시 ' + title

                # 소티디자인 상품리스트
                if title.count('소티디자인') > 0:
                    title = '소티디자인 ' + title

                # 키스홈 상품리스트
                if title.count('키스홈') > 0:
                    title = '키스홈 ' + title

                # 한솔종합목재(바우미스트) 상품리스트
                if title.count('바우미스트') > 0:
                    title = '바우미스트 ' + title

                # 세양침대 상품리스트
                if title.count('베디스') > 0:
                    title = '베디스 ' + title

                # (주)프로텍트어베드 상품리스트
                if title.count('프로텍트어베드') + title.count('마르셀린') > 0:
                    title = '(주)프로텍트어베드 ' + title

                # 주식회사럼블 상품리스트
                if title.count('제이픽스') > 0:
                    title = '주식회사럼블 ' + title

                # 청송방 상품리스트
                if title.count('바이안') + title.count('헬리빈') + title.count('굿더치커피') + title.count('솔로몬') > 0:
                    title = '청송방 ' + title

                # (주)드림파트너 상품리스트
                if title.count('디자이너스룸') + title.count('스페이스 1600'):
                    title = '(주)드림파트너 ' + title

                # 씨엠지(CMG) 상품리스트
                if title.count('올인원 독립 포켓스프링') > 0:
                    title = '씨엠지(CMG) ' + title

                # (주) 디에스피
                if title.count('DSP') > 0:
                    title = '(주) 디에스피 ' + title

                # 금지어확인1
                ck_code1 = False
                for ck in pass_title:
                    if title.count(ck) > 0:
                        ck_code1 = True
                        break

                # 처리상태
                td = trs.find_all('td')
                for tds in td:
                    try:
                        stateT = tds.find('div')
                        if stateT['title'] == '주문 상품별 주문 상태':
                            state = stateT.text
                    except:
                        pass

                # 금지어확인2
                ck_code2 = False
                for ck in pass_state:
                    if state.count(ck) > 0:
                        ck_code2 = True
                        break


                if ck_code1 == False and ck_code2 == False:

                    # 개별 상품명 컨트롤
                    if title.count("낮은 틈새 베란다 거실") > 0 or title.count("00블라인드") > 0 or title.count("팬트리장 속 깊은 냉장고") > 0 or title.count("템바 LED 화장대 의자") > 0:
                        title = '도아르 ' + title
                    elif title.count("슈가 주방 상하") > 0 or title.count("하이브리드 1인가구 멀티옷장") > 0:
                        title = '코코미 ' + title

                    # 업체명
                    cpy = title
                    cpy = cpy.split(' ')[0]

                    # 상품명에서 업체명 제거
                    title = title.replace(cpy, '').strip()


                    # 옵션명
                    try:
                        opt = trs.find(
                            'div', class_='option_info').text.replace('\n', '')
                        while True:
                            opt = opt.replace('  ', ' ')
                            if opt.count('  ') == 0:
                                break
                    except:
                        opt = ' '

                    # 주문수
                    cnt = trs.find('td', class_='goods_cnt').text

                    # 상품가
                    td = trs.find_all('td')
                    for tds in td:
                        if tds.text.count('0원') > 0:
                            price = tds.text.replace('원', '').replace(',', '')
                            break

                    # save temp
                    temp = []
                    temp.append(date)
                    temp.append(cpy)
                    temp.append(f'{img}#{url}')
                    temp.append(f'{title}#{opt}')
                    temp.append(cnt)
                    temp.append(price)
                    temp.append(state)
                    temp.append(ttime)

                    # save lists
                    lists.append(temp)




            # 콤마 제거
            for i in range(len(lists)):
                for j in range(len(lists[i])):
                    lists[i][j] = lists[i][j].replace(', ', '_').replace(',', '')




            # 주식회사_홍시, 매트리스 처리
            lists_temp = []
            for i in range(len(lists)):
                if lists[i][1] == '매트리스' and lists[i-1][1] == '매트리스' and lists[i-2][1] == '주식회사_홍시' and lists[i][7] == lists[i-1][7] == lists[i-2][7]:
                    lists[i-2][5] = int(lists[i-2][5]) + int(lists[i][5])
                elif lists[i][1] == '매트리스' and lists[i-1][1] == '주식회사_홍시' and lists[i][7] == lists[i-1][7]:
                    lists[i-1][5] = int(lists[i-1][5]) + int(lists[i][5])

                if lists[i][1] != '매트리스':
                    lists_temp.append(lists[i])

            lists = lists_temp


            # # save temp
            # with open('save_temp.csv', 'w', newline='', encoding='utf-8-sig') as f:
            #     write = csv.writer(f)
            #     write.writerows(lists)
            # print('done')




            # 가구 (구분) 그 외
            except_cpy = ['해담솔', '(주)안산동서물류', '이지드롭', 'KN디지털', '트라이스', '커피', '헬리빈', 'DoKDoK', '인덕션', '선풍기', '제습기', '써큘레이터', '건조기', '전기오븐', '탄소매트', '가습기', '온풍기', '난로', '전기포트', '보풀제거', '스팀다리미', '캠핑밥솥', '공기청정기', '밀대청소기', '스팀분사기', '와플기계', '에어프라이어', '전기냄비', '물걸레청소기']
            except_cpy_except = ['온우리가구', '주식회사럼블']
            for i in range(len(lists)):
                except_cnt = 0
                for j in range(len(except_cpy)):
                    if lists[i][1].count(except_cpy[j]) + lists[i][3].count(except_cpy[j]) > 0 and lists[i][1].count(except_cpy_except[0]) == 0 and lists[i][1].count(except_cpy_except[1]) == 0:
                        except_cnt += 1
                if except_cnt > 0:
                    lists_1.append(lists[i])
                else:
                    if lists[i][1] == "서라운드" or lists[i][1] == "전신거울도어":
                        lists[i][3] = lists[i][1] + " " + lists[i][3]
                        lists[i][1] = lists[i-1][1]
                    lists_2.append(lists[i])

            print('first_done')
            print('second_start')
            # setting_url2
            # 결합상품
            url_add = 'http://gdadmin.edftr76860385.godomall.com/order/order_list_all.php?detailSearch=n&scmFl=all'
            url_add = url_add + \
            f'''&key[]=o.orderNo&keyword[]=&key[]=o.orderNo&keyword[]=&key[]=o.orderNo&keyword[]=&goodsKey=og.goodsNm&goodsNo=&goodsText=결합상품&treatDateFl=og.regDt&searchPeriod=89&treatDate[]={month6}&treatTime[]=00:00:00&treatDate[]={today}&treatTime[]=23:59:59&orderStatus[]=o1&orderStatus[]=p1&orderStatus[]=g1&orderStatus[]=d1&orderStatus[]=d2&orderStatus[]=s1&invoiceCompanySno=0&invoiceNoFl=&orderMemoCd=&memFl=&settlePrice[]=&settlePrice[]=&receiptFl=&overDepositDay=&underDeliveryDay=&sort=og.orderNo+desc&pageNum={data_EA}&view=orderGoods&searchFl=y&applyPath=/order/order_list_all.php?view=orderGoods'''
            # print(url_add)

            # 검색
            driver.get(url_add)
            driver.implicitly_wait(1000)

            #html 들고오기
            htmll = driver.page_source
            soup_origin = bs(htmll, 'html.parser')
            soup = soup_origin.find('div', class_='table-responsive')

            tbody = soup.find('tbody')
            tr = tbody.find_all('tr', class_='text-center')

            pass_title = ['교환', '환불', '반품']
            pass_state = ['중단', '환불', '실패', '취소', '반품']


            for trs in tr:
                # 날짜
                date = trs.find('td', class_='font-date nowrap').text.strip()[:10]

                # 시간
                ttime = trs.find('td', class_='font-date nowrap').text.strip()[10:]

                # 주소
                url = trs.find('td', class_='text-left').find('a')['href']

                # 이미지
                img = trs.find('td', class_='text-left').find('img')['src']

                # 상품명
                title = trs.find(
                    'a', class_='one-line bold mgb5').text.replace('\n', '')

                title = title.replace('[결합상품] ','')

                # replace_word1
                # title = title.split(' ')[0].replace("]", " ").replace("[","")
                # while True:
                #     title = title.replace('  ', ' ')
                #     if title.count('  ') == 0:
                #         break


                # 금지어확인1
                ck_code1 = False
                for ck in pass_title:
                    if title.count(ck) > 0:
                        ck_code1 = True
                        break

                # 처리상태
                td = trs.find_all('td')
                for tds in td:
                    try:
                        stateT = tds.find('div')
                        if stateT['title'] == '주문 상품별 주문 상태':
                            state = stateT.text
                    except:
                        pass
                # 금지어확인2
                ck_code2 = False
                for ck in pass_state:
                    if state.count(ck) > 0:
                        ck_code2 = True
                        break

                if ck_code1 == False and ck_code2 == False:

                    # 처리상태
                    td = trs.find_all('td')

                    # 업체명
                    cpy = title.split(' ')[0]

                    for tds in td:
                        # 상품 상태
                        state = soup.find('div', {'title': '주문 상품별 주문 상태'}).text.strip()
                        # # 업체명
                        # cpy = title.split(' ')[0]

                        # 상품명에서 업체명 제거
                        title = title.replace(str(cpy), '').strip()



                        # 옵션명
                        try:
                            opt = trs.find('div', class_='option_info').text.replace('\n', '')
                            while True:
                                opt = opt.replace('  ', ' ').replace(',','')
                                if opt.count('  ') == 0:
                                    break

                        except:
                            opt = ' '

                        # 주문수
                        cnt = trs.find('td', class_='goods_cnt').text

                        # 상품가
                        td = trs.find_all('td')
                        for tds in td: #td
                            if tds.text.count('0원') > 0:
                                price = tds.text.replace('원', '').replace(',', '')
                                break

                        # save temp
                        temp = []
                        temp.append(date)
                        temp.append(cpy)
                        temp.append(f'{img}#{url}')
                        temp.append(f'{title}#{opt}')
                        temp.append(cnt)
                        temp.append(price)
                        temp.append(state)
                        temp.append(ttime)


                        # save lists
                    lists.append(temp)
                    lists_1.append(temp)
                    print(lists)
                    print(lists_1)



            # setting date
            for i in range(len(lists)):
                if int(lists[i][7][:2]) >= 17 and int(lists[i][7][:2]) <= 23:
                    cal_date = (datetime.strptime(
                        lists[i][0], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")
                    lists[i].append(lists[i][0])
                    lists[i][0] = cal_date
                else:
                    lists[i].append(lists[i][0])



            # list_test csv파일로 저장
            with open('brand.csv', 'w', newline='', encoding='utf-8-sig') as f:
                write = csv.writer(f)
                write.writerows(lists)

            # list_test csv파일로 저장
            with open('brand_1.csv', 'w', newline='', encoding='utf-8-sig') as f:
                write = csv.writer(f)
                write.writerows(lists_1)

            # list_test csv파일로 저장
            with open('brand_2.csv', 'w', newline='', encoding='utf-8-sig') as f:
                write = csv.writer(f)
                write.writerows(lists_2)

            print(f'수집완료 {now}')

    def ftp_trans():

        import ftplib
        url = 'http://priceflow.co.kr'
        dir = '/html/ds/df/br/'
        session = ftplib.FTP()
        session.connect('112.175.185.27', 21)
        session.encoding = 'utf-8'
        session.login("dailyroutine85", "dpg85kjp#")
        session.cwd(dir)

        uploadFiles = ['brand.csv', 'brand_1.csv', 'brand_2.csv', 'index.html', 'index_1.html', 'index_2.html', 'index_all.html']
        for files in uploadFiles:
            with open(file=files, mode='rb') as wf:
                session.storbinary(f'STOR {files}', wf)


    # Main
    while True:
        try:
            get(driver)
            ftp_trans()
            break
        except:
            pass



# step3.실행 주기 설정
schedule.every(1).hours.do(main)

# step4.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(1)

main()


