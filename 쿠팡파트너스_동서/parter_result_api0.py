from datetime import datetime, timedelta
now = datetime.now()
before_one_day = (now - timedelta(days=30)).strftime('%y%m%d')

END = "20" + now.strftime('%y%m%d')
START = "20" + before_one_day

date = END + " " + START
text_file = open("date.txt", "w", encoding='utf-8-sig')
text_file.write(date)