import datetime
import pytz

def time():
    pacific = pytz.timezone('US/Pacific')
    now = datetime.datetime.now(tz=pacific)
    time = f'{now.month}' + '/' + f'{now.day}' + '/' + f'{str(now.year)[2:]}'
    return time
