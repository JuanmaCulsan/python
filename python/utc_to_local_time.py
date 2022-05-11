import datetime
from posixpath import split
import time
import pytz
import tzlocal
import requests


current_local_time = datetime.datetime.now()
print("Current Local Time: ", current_local_time)

current_utc_time = datetime.datetime.utcnow()
print ("Current UTC Time: ", current_utc_time)

local_timezone = tzlocal.get_localzone()
print ("local_timezone: ", local_timezone)

a = current_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

#print ("Current UTC Time to Local Time: ", current_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone))

print(type(a))
b = str(a)
print(type(b))
print(b)

c = b.split("+")
print(c[0]+"z")