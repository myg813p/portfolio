global URL
global START
global END
global sch
sch = ''

def api_json():
    global sch
    import hmac
    import hashlib
    import os
    import time
    import requests
    import pprint
    import json


    def coupang_api(WHAT):
        global sch

        REQUEST_METHOD = "GET"
        DOMAIN = "https://api-gateway.coupang.com"
        ACCESS_KEY = 'd41d0ed7-3c53-4ca0-83db-e1bb585e268e'         # 동서가구 A_Key
        SECRET_KEY = '11588f33eda8c03ebd714af7542c68eafd2731df'     # 동서가구 S_Key

        def generateHmac(method, secretKey, accessKey):
            global URL
            global START
            global END
            global sch

            os.environ["TZ"] = "GMT+0"
            datetime2 = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'

            #date가져오기 ###   #################   #################
            from datetime import datetime, timedelta
            now = datetime.now()
            before_one_day = (now - timedelta(days=30)).strftime('%y%m%d')

            END = "20" + now.strftime('%y%m%d')
            START = "20" + before_one_day

            ck_time = int(time.strftime('%H%M%S')) + 90000
            print(ck_time)
            if ck_time < 120000  or ck_time > 180000:
                sch = False
                return sch
            else:
                sch = True
            #################   #################   #################


            parmas = f"?startDate={START}&endDate={END}"
            URL = f"/v2/providers/affiliate_open_api/apis/openapi/v1/reports/{WHAT.split('#')[-1]}{parmas}"
            path, *query = URL.split("?")
            message = datetime2 + method + path + (query[0] if query else "")

            signature = hmac.new(bytes(secretKey, "utf-8"),
                                message.encode("utf-8"),
                                hashlib.sha256).hexdigest()

            return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime2, signature)
        if sch == False:
            return

        authorization = generateHmac(REQUEST_METHOD, SECRET_KEY, ACCESS_KEY)
        try:
            url = "{}{}".format(DOMAIN, URL)
        except:
            return

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


    # #START END
    # with open("date.txt", 'r', newline='', encoding='utf-8-sig') as f:
    #     txt = f.readline()
    # END = int(txt.split(" ")[0])
    # START = int(txt.split(" ")[1])
    # print(START)
    # print(END)


    ##
    for i in range(1,5):
        WHAT = dic[i]

        test = coupang_api(WHAT)
        if sch == False:
            return
        pprint.pprint(test.json())

        with open(f'{WHAT.split("#")[0]}.json', 'w', encoding='UTF-8') as outfile:
            json.dump(test.json(), outfile, ensure_ascii=False)

def api_csv():
    global START
    global END
    import json
    from datetime import datetime, timedelta
    import csv

    fn_list = []

    END = END[0:4] +"-" + END[4:6] + "-" + END[6:8]
    START = START[0:4] +"-" + START[4:6] + "-" + START[6:8]
    def date_range(start, end):
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
        return dates
    dates = date_range(START, END)
    for i in range(len(dates)):
        dates[i] = dates[i].replace("-","")
    # print(dates)




    #클릭량
    with open("클릭량.json", 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    lists = data["data"]
    # for ls in lists:
    #     print(ls)
    for i in range(len(dates)):
        click = 0
        for j in range(len(lists)):
            if dates[i] == lists[j]['date']:
                click = click + lists[j]['click']
        fn_list.append([str(dates[i]), str(click)])
    # print(fn_list)


    #주문량
    with open("주문량.json", 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    lists = data["data"]
    # for ls in lists:
    #     print(ls)


    #취소량
    with open("취소량.json", 'r', encoding='utf-8-sig') as file:
        c_data = json.load(file)
    c_lists = c_data["data"]
    # for ls in lists:
    #     print(ls)

    #주문량 - 취소량
    for i in range(len(c_lists)):
        for j in range(len(lists)):
            if c_lists[i]['orderDate'] == lists[j]['date'] and\
                c_lists[i]['productName'] == lists[j]['productName']:
                    lists[j]['quantity'] = lists[j]['quantity'] + c_lists[i]['quantity']
                    lists[j]['gmv'] = lists[j]['gmv'] + c_lists[i]['gmv']
                    lists[j]['commission'] = lists[j]['commission'] + c_lists[i]['commission']



    #최종 리스트
    for i in range(len(fn_list)):
        quantity = 0
        gmv = 0
        commission = 0
        for j in range(len(lists)):
            if fn_list[i][0] == lists[j]['date']:
                quantity = quantity + lists[j]['quantity']
                gmv = gmv + lists[j]['gmv']
                commission = commission + lists[j]['commission']
        fn_list[i].append(str(int(quantity)))
        fn_list[i].append(str(int(gmv)))
        fn_list[i].append(str(int(commission)))
    #print(fn_list)



    #상품명 리스트
    title_list = []
    for i in range(len(lists)):
        if int(lists[i]['quantity']) != 0:
            title_list.append([lists[i]['date'], str(lists[i]['productName']).replace(',','/'), str(int(lists[i]['quantity'])), str(int(lists[i]['gmv'])), str(int(lists[i]['commissionRate'])), str(int(lists[i]['commission']))])
    #print(title_list)


    #make csv
    #list_test csv 파일세로로 저장
    with open('fn_list.csv', 'w', newline='', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        for item in fn_list:
            write.writerow(item)

    #list_test csv 파일세로로 저장
    with open('title_list.csv', 'w', newline='', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        for item in title_list:
            write.writerow(item)



    #FTP
    import ftplib
    try:
        url = 'http://priceflow.co.kr'
        dir = '/html/ds/cp/data/'
        session = ftplib.FTP()
        session.connect('112.175.185.27', 21)
        session.encoding = 'utf-8'
        session.login("dailyroutine85", "dpg85kjp#")
        session.cwd(dir)
        # print(session.nlst())

        uploadFiles = ['fn_list.csv', 'title_list.csv', "index.html", "index9.css"]
        for files in uploadFiles:
            with open(file=files, mode='rb') as wf:
                session.storbinary(f'STOR {files}', wf)

    except Exception as e:
        print('error')
        print(e)
    print('done')

#main
def main():
    global sch
    api_json()
    if sch == False:
        return
    api_csv()


while True:
    print('try')
    main()
    print('It will be start at 12:00~13:30')
    sch = True
    import time
    time.sleep(86400)