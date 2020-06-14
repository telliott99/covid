import sys, os, csv
from ustrings import sep
from udates import all_dates
import ukeys

base = os.environ.get('covid_base')
sys.path.insert(0,base)

src = 'csv.source'
db = 'db.txt'

def list_directory(d):
    dL = os.listdir(d)
    dL = [e for e in dL if not e.startswith('.')]   
    dL.sort()
    return dL
        
# file stuff

def read_csv_data_file(fn):
    print 'reading:  ', fn
    D = {}
    with open(fn) as fh:
        data = fh.read()
    data = data.strip().split('\n')[1:]
    
    reader = csv.reader(data)
    for e in reader:
        fips,county,state,country = e[:4]
        if len(fips) == 4 and country == 'US':
            fips = '0' + fips
            
        k = sep.join([county,state,fips,country])
        
        # it's too much trouble to keep cols I don't use
        # D[k] = ','.join(e[7:11])
        
        # change '-' to 0 later
        cases = e[7]
        deaths = e[8]
        D[k] = {'cases':cases, 'deaths':deaths}
    return D

def dict_from_data(data):
    D = {}
    for entry in data:
        vL = entry.strip().split('\n')
        k = vL[0]
        cases = vL[1]
        deaths = vL[2]
        if ',' in cases:
            cases = cases.strip().split(',')
            deaths = deaths.strip().split(',')
        else:
            cases = [cases]
            deaths = [deaths]
            
        cases = [int(c) for c in cases]
        deaths = [int(c) for c in deaths]
        
        D[k] = { 'cases': cases, 'deaths': deaths}
    return D

def load_db(fn = db):
    with open(fn) as fh:
        data = fh.read().strip().split('\n\n')
    date_info = data[0]
    data = data[1:]    
    D = dict_from_data(data)
    return date_info, D
    
def save_db(D):
    first = all_dates[0]
    last = all_dates[-1]

    pL = [first + '\n' + last]
    for k in sorted(D.keys(), cmp = ukeys.custom_sort):
        cases = [str(n) for n in D[k]['cases']]
        deaths = [str(n) for n in D[k]['deaths']]
    
        tmp = k + '\n'
        tmp += ','.join(cases) + '\n'
        tmp += ','.join(deaths) + '\n'
        pL.append(tmp)
    
    with open(db,'w') as fh:
        fh.write('\n\n'.join(pL))

    
