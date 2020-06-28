import sys, os
from datetime import date, datetime, timedelta

base = os.environ.get('covid_base')
sys.path.insert(0,base)

from myutil.ufile import list_directory

'''
dates are a bit tricky
there is the format issue
2020-03-22 v. 03-22 v. 03/22

there is also the question of the first date

originally it was 2020-03-22
now it is usually the first dated file in 'csv.source'

If we're building the database
the first date should be a variable

Otherwise, get the first date from the db

All this module does is provide generate_dates

'''

# format = 2020-03-25
def generate_dates(first=None):
    if not first:
        first = '2020-03-22'
        
    today = str(date.today())
    #print('udates:  first', first)
    
    L = list()
    start = datetime.strptime(first, '%Y-%m-%d')
    end   = datetime.strptime(today, '%Y-%m-%d')
    step  = timedelta(days=1)

    while start < end:   
        # can't get today's data until tomorrow, hence <
        L.append(str(start.date()))
        start += step 
    return L
    
#-------------------------------------
  
def date_from_path(p, short=False):
    if '/' in p:
        p = p.strip().split('/')[-1]
    p = p.split('.')[0]
    if short:
        return p.split('-',1)[1]  
    return p
    
def slash_dates(dL):
    return [e.split('-',1)[1].replace('-','/')[1:] for e in dL]

def date_slice(date_info,conf):
    last = date_info.split()[1]
    i = all_dates.index(last)
    n = conf['n']
    
    dates = all_dates[i-n+1:i+1]
    dates = [e[-5:].replace('-','/') for e in dates]
    return dates