import sys, os, csv

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
util = base + '/myutil'
if not util in sys.path:
    sys.path.insert(0, util)
    
sep = ';'
sep2 = '#'

import udates, ukeys

#import udates, ukeys
from udates import generate_dates

def read_csv_data_file(fn):
    print('reading:  %s' % udates.date_from_path(fn))
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

def load_db(path_to_db):
    with open(path_to_db) as fh:
        data = fh.read().strip().split('\n\n')
        
    date_info = data[0]
    data = data[1:]    
    D = dict_from_data(data)
    return date_info, D
    
def save_db(D, path_to_db, first, last):
    #all_dates = generate_dates()
    #first = all_dates[0]
    #last = all_dates[-1]

    pL = [first + '\n' + last]
    for k in sorted(D.keys(), key = ukeys.custom_key):
        cases = [str(n) for n in D[k]['cases']]
        deaths = [str(n) for n in D[k]['deaths']]
    
        tmp = k + '\n'
        tmp += ','.join(cases) + '\n'
        tmp += ','.join(deaths) + '\n'
        pL.append(tmp)
    
    with open(path_to_db,'w') as fh:
        fh.write('\n\n'.join(pL))

#---------------
    
def refmt(key):
    sL = key.split(sep)  # works w/ or w/o fips, US
    county = sL[0]
    state = sL[1]
    #state = us_states[state]
    cs = county + ', ' + state
    return cs

#---------------
'''
def get_popD():
    # load population data
    fn = base + '/population/pop.csv'
    with open(fn) as fh:
        pop_data = fh.read().strip().split('\n')
        
    pD = {}
    for e in pop_data:
        loc,population = e.split(',')
        k = refmt(loc)
        pD[k] = population
    return pD
'''