import csv
from datetime import datetime, timedelta


#csv파일 list로 불러오기
with open('brand.csv', 'r', newline='', encoding='utf-8-sig') as f:
    read = csv.reader(f)
    lists = list(read)


for i in range(len(lists)):
    if int(lists[i][7][:2]) >= 17 and int(lists[i][7][:2]) <= 23:
        print(lists[i][7])
        cal_date = (datetime.strptime(lists[i][0], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")
        lists[i].append(lists[i][0])
        lists[i][0] = cal_date
    else:
        lists[i].append(lists[i][0])

print(lists)


#list_test csv파일로 저장
with open('brand2.csv', 'w', newline='', encoding='utf-8-sig') as f:
    write = csv.writer(f)
    write.writerows(lists)