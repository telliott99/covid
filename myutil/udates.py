from datetime import date, datetime, timedelta

today = str(date.today())
first = '2020-05-01'   # specifies the first date for the db

def generate_dates():
    L = list()
    start = datetime.strptime(first, '%Y-%m-%d')
    end   = datetime.strptime(today, '%Y-%m-%d')
    step  = timedelta(days=1)

    while start < end:   
        # can't get today's data until tomorrow, hence <
        L.append(str(start.date()))
        start += step
    return L

all_dates = generate_dates()
last = all_dates[-1]

def list_directory(d):
    dL = os.listdir(d)
    dL = [e for e in dL if not e.startswith('.')]   
    dL.sort()
    return dL
    
def date_from_fn(fn):
    return fn.split('-',1)[1].split('.')[0]
    
def slash_dates(dL):
    return [e.split('-',1)[1].replace('-','/')[1:] for e in dL]



def date_slice(date_info,conf):
    last = date_info.split()[1]
    i = all_dates.index(last)
    n = conf['n']
    
    dates = all_dates[i-n+1:i+1]
    dates = [e[-5:].replace('-','/') for e in dates]
    return dates