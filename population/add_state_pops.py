import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.udb as udb
import myutil.ukeys as ukeys
import myutil.ustates as ustates
import myutil.ustrings as ustrings

path_to_db = base + '/db.txt'
sep = ustrings.sep
    
def get_county_pop_dict(D):
    # initial version, test file w/
    # Autauga;Alabama,55869 ..
    
    path = 'pop.txt'
    with open(path) as fh:
        data = fh.read()
    
    pD = {}
    for line in data.strip().split('\n'):
        print(line)
        k,pop = line.strip().split('#')
        pD[k] = pop
         
    s = '''
    ;Diamond Princess
    ;Grand Princess
    Federal Correctional Institution (FCI);Michigan
    Michigan Department of Corrections (MDOC);Michigan
    ;Recovered
    '''
    sL = s.strip().split('\n')
    sL = [s.strip() for s in sL]

    # using county;state;fips;US keys
    for k in D:
        if not k.endswith(sep + 'US'):
            continue
        if k.startswith('Unassigned'):
            continue
        if k.startswith('Out of '):
            continue
            
        short = sep.join(k.split(sep)[:2])
        if short in sL:
            continue
    
        # we'll pick up these guys separately        
        tL = [';Guam',';Puerto Rico',';Virgin Islands']
        tL += [';Northern Mariana Islands']
        if short in tL:
            continue
        
        # use long form for keys (same as main db)
        # find the data from the short form
        pD[k] = pD[short]
        
        # remove the short keys
        ukeys.popif(pD,short)
        
    return pD
    
def modify_county_pop_dict(county_pop_dict):
    sD = ustates.state_to_pop
    for k in sD:
        pop = sD[k]
        try:
            abbrev = ustates.state_to_abbrev[k]
        except KeyError:
            tabbrev = ustates.terr_to_abbrev[k]
        fips = ustates.abbrev_to_fips[abbrev]
        full = sep.join(['',k,fips,'US'])
        county_pop_dict[full] = pop
        
def get_pop_dict(D):
    
    cD = get_county_pop_dict(D)
    modify_county_pop_dict(cD)
    return cD

if __name__ == "__main__":
    date_info, D = udb.load_db(path_to_db)
    
    cD = get_pop_dict(D)
    for k in cD:
        if len(k.split(sep)) < 4:
            print(k)
    
    '''
    #print(cD.keys())
    
    for k in sorted(cD, key = ukeys.custom_key):
        if k.startswith(sep):
            print(k, pop_dict[k])
'''