from datetime import datetime
import pytz

my_datetime = datetime(2023, 2, 13, 17, 10, 27, tzinfo = pytz.utc)
print(my_datetime)

my_datetime_utc = my_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z')
print(my_datetime_utc)

my_datetime_cet = my_datetime.astimezone(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
print(my_datetime_cet)

