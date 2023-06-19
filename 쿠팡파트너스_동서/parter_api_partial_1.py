import time
import re
import html
from bs4 import BeautifulSoup
import requests
import csv



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

#url
#url
#url
#url
#url
#url
#url
url = 'https://pages.coupang.com/p/79929?src=1139000&spec=10799999&addtag=600&ctag=79929&lptag=AF5175956&itime=20230117142607&pageType=EVENTPAGE&pageValue=79929&wPcid=16532709741816198565144&wRef=www.dongsuhfurniture.co.kr&wTime=20230117142607&redirect=landing&traceid=V0-181-856067a1509fbb08&placementid=&clickBeacon=&campaignid=&contentcategory=&imgsize=&pageid=&deviceid=&token=&contenttype=&subid=&impressionid=&campaigntype=&requestid=&contentkeyword=&subparam='
#url
#url
#url
#url
#url
#url
#url
#url
#url
#url


with open("htmll.html", 'r', newline='', encoding='utf-8-sig') as f:
    htmlL = f.readlines()
htmll =''
for htmls in htmlL:
    htmll += htmls




try:
    # res = requests.get(url, verify=False, headers=headers)
    # htmll = html.unescape(res.text)
    soup = BeautifulSoup(htmll, 'html.parser')

    elems = soup.find_all('li', class_='recommend-widget__item c-product')
    print(len(elems))
    #print(elems[0])

    all_list = []
    cnt = 0
    for i in range(len(elems)):

        # 0링크
        link = (elems[i].find('a')['href']).replace('https://www.','https://m.').replace('/vp/', '/vm/').replace('&isAddedCart=', '')
        #print(link)
        # link = short_url(link)

        if link.count('없음') == 0:
            #
            temp_list = []

            # 1상품 이미지
            img = elems[i].find('div', class_='recommend-widget__item__image-wrap')
            thumbnail = 'https:' + elems[i].find('img')['src']
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

            print(temp_list)
            time.sleep(1000)

            print(f'{i+1}/{len(elems)}')
            cnt += 1
            if i >= 5:
                print(f'상품 {cnt} 건 수집완료')
                break
        else:
            pass
    print(f'상품 {cnt} 건 수집완료')

    list_to_html = str(all_list)
    list_to_html = list_to_html.replace('[[','').replace(']]','')
    list_to_html = list_to_html.replace('[','').replace('],',',,')
    list_to_html = list_to_html.replace("',",',,')
    list_to_html = list_to_html.replace("'",'')

    #html 저장
    with open("list_html.html", 'w', newline='', encoding='utf-8-sig') as f:
        f.write(list_to_html)
    print('저장')
except:
    pass
