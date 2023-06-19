import time
import csv



#csv파일 list로 불러오기
with open('cp_list.csv', 'r', newline='', encoding='utf-8-sig') as f:
    read = csv.reader(f)
    read_test = list(read)
print(len(read_test))
print(read_test[0])


html_top = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Document</title>
</head>

<body >
    <section class="cards" style="display: flex; flex-wrap: wrap; justify-content: space-between;">'''


html_mid = ''
for i in range(len(read_test)):
    read_test[i][1] = read_test[i][1][:40]

    if read_test[i][6] != 'none':
        read_test[i][6] = f'<img class="card-rocket" src="{read_test[i][6]}" alt="로켓배너" style="height:16px;width: auto;">'
    else:
        read_test[i][6] = ''


    mid_EA = f'''        <article class="card" style="max-width: calc(30% -  250px); flex: 1 0 200px; margin: 1rem .25em; width: 250px; height: 320px;">
            <a href="{read_test[i][0]}"><img class="card-img-top"
                src="{read_test[i][2]}"
                alt="대표이미지"></a>
            <div class="card-body">
                <a class="card-title" style="font-family:arial,맑은 고딕;font-size: 12px;text-decoration: none;color:black;">{read_test[i][1]}</a>

                <br>
                <a class="card-price"
                    style="list-style: none;text-align: left;font-style: normal;line-height: 20px;color: #ae0000;font-size: 16px;font-family: Tahoma,sans-serif;font-weight: 1000;text-decoration: none;">{read_test[i][5]}</a>
                {read_test[i][6]}
            </div>
        </article>'''
    html_mid = html_mid + mid_EA

html_bottom = '''    </section>


    </div>
</body>

</html>>'''


html = html_top + html_mid + html_bottom

with open("show.html", 'w', newline='', encoding='utf-8-sig') as f:
    f.write(html)