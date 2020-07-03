#python3 extract_pop.py > pop.db.txt

import sys, os, csv
base = os.environ.get('covid_base')
sys.path.insert(0,base)

from do_imports import *

path_to_db = base + '/db.max.txt'
date_info, D = udb.load_db(path_to_db)

sep = udb.sep

#------------------

def fix_Virginia(county):
    va_cities = ['Charles City',
        'Fairfax City', 'Franklin City',
        'James City', 'Richmond City',
        'Roanoke City']
        
    if county in va_cities:
        return county
    return county.replace(' City','')

def get_pop_data():
    fn = base + '/population/data/co-est2019-annres.csv'
    #fn = 'co-est2019-annres.csv'
    with open(fn) as fh:
        data = fh.read().strip().split('\n')
    
    # remove United States summary
    pL = []
    reader = csv.reader(data[1:])
    for e in reader:
        if e[0].startswith('.'):
            e[0] = e[0][1:]
        county, state = e[0].split(',')
        state = state.strip()    
        county = county.strip()
        pop = e[-1].replace(',','')
        
        alts = ['County', 'Census Area', 
                 'City and Borough',
                'Borough', 'Municipality',
                'Parish' ]
                
        for sfx in alts:
            if county.endswith(sfx):
                county = county.replace(sfx,'').strip()
        if county.endswith('city'):
            county = county.replace('city','City')
            
        if county == 'New York':
            county += ' City'
        
        if state == 'Virginia':
            county = fix_Virginia(county)
            
        if county == 'Washington' and state == 'Utah':
            county += ' County'    # db has County
        
        loc = ';'.join([county,state]) + ';'
        pL.append((loc,pop))
        
    return pL

pL = get_pop_data()

#----------------------------

def test():
    for loc, pop in pL:
        rL = []
        for k in D:
            if k.startswith(loc):
                rL.append(k)
        if len(rL) != 1:
            print(short, rL)

# now we need to add fips if the key has it

def get_pop_dict(pL,D):
    pop_dict = {}
    for loc, pop in pL:
        for k in D:
            if k.startswith(loc):
                pop_dict[k] = pop
                break
    return pop_dict
    
pD = get_pop_dict(pL,D)

#----------------------------

with open(base + '/population/extra.txt') as fh:
    for e in fh.read().strip().split('\n'):
        if e == '':
            continue
        k,pop = e.strip().split('#')
        pD[k] = pop

def filter(k):
    if k.startswith('Unassigned'):
        return False
    if k.startswith('unassigned'):
        return False
    if k.startswith('Out of'):
        return False
    if 'Unknown' in k or 'Recovered' in k:
        return False
    if 'Princess' in k or 'Out-of' in k:
        return False
    if 'MDOC' in k or 'FCI' in k:
        return False
    return True
    
pD[';American Samoa;60;US'] = 55641
pD[';Puerto Rico;72;US'] = 3193694
pD[';Guam;66;US'] = 165718
pD[';Virgin Islands;78;US'] = 104914
pD[';Northern Mariana Islands;69;US'] = 55194


pD['Southwest Utah;Utah;90049;US'] = 239105
pD['Brockton;Massachusetts;;US'] = 95703
pD['Nashua;New Hampshire;;US'] = 89246
pD['Elko County;Nevada;32007;US'] = 20341
pD['Desoto;Florida;;US'] = 38001
pD['Garfield County;Washington;53023;US'] = 2247
pD['Washington;Utah;49053;US'] = 19249
pD['Manchester;New Hampshire;;US'] = 112525
pD['Dukes and Nantucket;Massachusetts;;US'] = 17332
ukeys.popif(pD,'Dukes and Nantucket;Massachusetts')


# any db keys not in pop dict?
def test2(pD,D):
    for k in D:
        if not k.endswith(';US'):
            continue
        if not filter(k):
            continue  
        if not k in pD:
            print(k)   
        
def add_states(pD):
    with open('data/states_by_population.txt') as fh:
        data = fh.read().strip().split('\n')
    data = [e for e in data if not e == '']

    for e in data:
        if e.startswith('#') or e.startswith('US'):
            continue
        state, pop = e.strip().split(',')
        try:
            abbrev = ustates.state_to_abbrev[state]
        except KeyError:
            abbrev = ustates.terr_to_abbrev[state]
        fips = ustates.abbrev_to_fips[abbrev]
        k = ';'.join(['',state,fips,'US'])
        pD[k] = pop

add_states(pD)

if __name__ == "__main__":
    test()
    # no output  every loc in pop data finds one key

    test2(pD,D)
    # no output  every key in db finds a pop
    
    kL = pD.keys()
    kL = sorted(kL, key=ukeys.custom_key)
    for k in kL:
        print(k + '#' + str(pD[k]))

    



