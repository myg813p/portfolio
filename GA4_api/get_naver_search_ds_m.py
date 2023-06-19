import requests
from bs4 import BeautifulSoup as bs
import time
import warnings

# Ignore the InsecureRequestWarning message
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made.")

url = 'https://m.search.naver.com/search.naver?query=동서가구'
res = requests.get(url)
soup = bs(res.text, 'html.parser')


body = soup.find('section', class_='sc sp_brand ad_light_mode')
# print(body)

hrefs = body.find_all('a')
print(len(hrefs))

for lk in hrefs:
    url = lk['href']
    res = requests.get(url, verify=False)
    lk['href'] = res.url

    ck_href = res.url.replace("https://www","m").split("&n_query=")[0] + '&n_query=동서가구'

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

#css
elems = soup.find_all('link')
css = ''
for el in elems:
    if el['href'].count('main.9ae0126b.css') or el['href'].count('w_new_230309.css'):
        css += str(el)

html = f'{css}{body}'
#save as html
with open("naver_m.html", 'w', newline='', encoding='utf-8-sig') as f:
    f.write(html)