import requests
from bs4 import BeautifulSoup as bs
import html
import time
import csv

#csv_file_set
with open('cp_list.csv', 'w', newline='', encoding='utf-8-sig') as f: pass



#csv파일 list로 불러오기
with open('get_gp.csv', 'r', newline='', encoding='utf-8-sig') as f:
    read = csv.reader(f)
    read_test = list(read)
print(read_test)
print(read_test[0][0])
print(len(read_test))

#main
for i in range(len(read_test)):
    temp_list = []
    #쿠팡 접속 해더
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}


    url = read_test[i][0]
    res = requests.get(url, verify=False, headers=headers)
    htmll = html.unescape(res.text)

    soup = bs(htmll, 'html.parser')

    title = soup.find('h2', class_='prod-buy-header__title').text.replace(',','').strip()
    print(title)

    img = soup.find('img', class_='prod-image__detail')['src']
    img_src = "https:" + img
    print(img_src)

    try:
        discount_rate = soup.find('span', class_='discount-rate').text.strip()
        print(discount_rate)

        origin_price = soup.find('span', class_='origin-price').text.strip()
        print(origin_price)
    except:
        discount_rate = 'none'
        origin_price = 'none'
        print(discount_rate)
        print(origin_price)

    total_price = soup.find('span', class_='total-price').text.replace(',','').replace('원','').strip()
    print(total_price)

    try:
        badge = soup.find('td', class_='td-delivery-badge')
        badge = "http:" + badge.find('img')['src']
    except:
        badge = 'none'
    print(badge)

    temp_list.append(read_test[i][0])   #url
    temp_list.append(title)
    temp_list.append(img_src)
    temp_list.append(discount_rate)
    temp_list.append(origin_price)
    temp_list.append(total_price)
    temp_list.append(badge)

    #list_test csv파일로 저장
    with open('cp_list.csv', 'a', newline='', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        write.writerows([temp_list])
    print(f'{i+1}/{len(read_test)}')
    time.sleep(7)
