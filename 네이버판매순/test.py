
import time

def get_from_naver():
    import requests
    import json


    lists = []
    cnt = 0
    before_list_cnt = 0
    while True:
        if cnt == 0:
            temp_lists = []
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://api.itemscout.io/api/best/subcategories/5'
            res = requests.get(url, headers=headers)
            data_json = json.loads(res.text)

            # print(data_json['data'])

            for i in range(len(data_json['data'])):
                # print(data_json['data'][i])
                temp_lists.append([data_json['data'][i]['id'], data_json['data'][i]['name']])
                lists.append([data_json['data'][i]['id'], data_json['data'][i]['name']])
        else:
            temp_lists2 = temp_lists
            temp_lists = []

            for all in range(len(temp_lists2)):
                headers = {'User-Agent': 'Mozilla/5.0'}
                url = f'https://api.itemscout.io/api/best/subcategories/{temp_lists2[all][0]}'
                res = requests.get(url, headers=headers)
                data_json = json.loads(res.text)
                # print(data_json['data'])
                print(url)
                if res.status_code == 200:
                    for i in range(len(data_json['data'])):
                        # print(data_json['data'][i])
                        temp_lists.append([data_json['data'][i]['id'], data_json['data'][i]['name']])
                        lists.append([data_json['data'][i]['id'], data_json['data'][i]['name']])

        cnt+=1
        print(f'\n\n{lists}\n\n')
        print(len(lists))
        print(f'cnt:{cnt}')
        if before_list_cnt == len(lists):
            break
        before_list_cnt = len(lists)


    print('done')


    #가구만 json 파일만들기
    file_name_fin = ''
    for cat in range(len(lists)):
        url = f'https://api.itemscout.io/api/best/product/list?cid={lists[cat][0]}&type=ORDER&days=14'
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        time.sleep(1)

        if res.status_code == 200:
            lists[cat][1] = lists[cat][1].replace('/', ',')
            file_name = f'{lists[cat][0]}_{lists[cat][1]}'
            file_name_fin += f'{file_name}#'

            with open(f"{file_name}.json", "w", encoding="utf-8") as file:
                file.write(res.text)


        print(f'{cat+1}/{len(lists)} : {lists[cat][0]}')

    with open("list_name.txt", "w", encoding="utf-8") as file:
        file.write(file_name_fin)

def ftp_up():
    import os
    import ftplib

    try:
        session = ftplib.FTP()
        session.connect('112.175.185.27', 21)
        session.encoding = 'utf-8'
        session.login("dailyroutine85", "dpg85kjp#")
        session.cwd('/html/ds/nvli/')
        print(session.nlst())



        # Set the directory path
        directory_path = 'C:/Users/DSF20220704001/OneDrive/바탕 화면/네이버판매순'

        # Get a list of all the items in the directory
        items = os.listdir(directory_path)

        # save uploadFiles
        uploadFiles = []
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                uploadFiles.append(item)
        # print(uploadFiles)

        for files in uploadFiles:
            with open(file=files, mode='rb') as wf:
                session.storbinary(f'STOR {files}', wf)
            print(files)

    except Exception as e:
        print('test')
        print(e)


get_from_naver()
ftp_up()