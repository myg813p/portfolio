from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

now = datetime.now()
today = now.strftime("%Y-%m-%d")
month = now - relativedelta(months=6)
# month = now - relativedelta(day=7)

month_minus_one_day = month + timedelta(days=2)
month6 = month_minus_one_day.strftime("%Y-%m-%d")


print(today)
print(month6)