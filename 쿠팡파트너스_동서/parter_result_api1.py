import hmac
import hashlib
import os
import time
import requests
import pprint
import json


def coupang_api(WHAT, START, END):
    REQUEST_METHOD = "GET"
    DOMAIN = "https://api-gateway.coupang.com"
    ACCESS_KEY = 'd41d0ed7-3c53-4ca0-83db-e1bb585e268e'         # 동서가구 A_Key
    SECRET_KEY = '11588f33eda8c03ebd714af7542c68eafd2731df'     # 동서가구 S_Key
    parmas = f"?startDate={START}&endDate={END}"
    URL = f"/v2/providers/affiliate_open_api/apis/openapi/v1/reports/{WHAT.split('#')[-1]}{parmas}"

    def generateHmac(method, url, secretKey, accessKey):
        path, *query = url.split("?")
        os.environ["TZ"] = "GMT+0"
        datetime = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
        message = datetime + method + path + (query[0] if query else "")

        signature = hmac.new(bytes(secretKey, "utf-8"),
                            message.encode("utf-8"),
                            hashlib.sha256).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime, signature)

    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }

    response = requests.get(url=url, headers=headers)
    return response


dic = {
    1:'클릭량#clicks',
    2:'주문량#orders',
    3:'취소량#cancels',
    4:'수익정보#commission',

    5:'배너클릭클릭량#ads/impression-click',
    6:'배너클릭주문량#ads/orders',
    7:'배너클릭취소량#ads/cancels',
    8:'배너클릭수익정보#ads/commission',
    9:'배너클릭eCPM#ads/performance',
}


#START END
with open("date.txt", 'r', newline='', encoding='utf-8-sig') as f:
    txt = f.readline()
END = int(txt.split(" ")[0])
START = int(txt.split(" ")[1])
print(START)
print(END)


##
for i in range(1,5):
    WHAT = dic[i]

    test = coupang_api(WHAT, START, END)
    pprint.pprint(test.json())

    with open(f'{WHAT.split("#")[0]}.json', 'w', encoding='UTF-8') as outfile:
        json.dump(test.json(), outfile, ensure_ascii=False)

