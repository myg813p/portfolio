import requests
from bs4 import BeautifulSoup as bs
import time

url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=동서가구'
res = requests.get(url)
soup = bs(res.text, 'html.parser')


body = soup.find('div', class_='brand_wrap')
hrefs = body.find_all('a')
for lk in hrefs:
    url = lk['href']
    res = requests.get(url, verify=False)
    lk['href'] = res.url

    ck_href = res.url.replace("https://","").split("&n_query=")[0]

    #count 확인 from test.html
    print(ck_href)


    try:
        class_name = lk['class'][0]
    except:
        class_name = 'pass'

    if class_name == 'link' or class_name == 'tit':
        lk.string = str(lk.string) + '(100)'
        lk['style'] = 'font-size:12px;color:red;'
    else:
        div_tag = soup.new_tag('p', attrs={'class': 'alert'})
        div_tag.string = '(100)'
        div_tag['style'] = 'font-size:12px;color:red;'
        lk.insert_after(div_tag)

print(str(body))

body = str(soup.find('div', class_='brand_wrap')).replace('<em>', '<br><em>')

elems = soup.find_all('link')
css = ''
for el in elems:
    if el['href'].count('main.c65ac745.css') or el['href'].count('search1_230216.css'):
        css += str(el)

html = f'{css}{body}'


#save as html
with open("naver.html", 'w', newline='', encoding='utf-8-sig') as f:
    f.write(html)