import sys, os

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
util = base + '/myutil'
if not util in sys.path:
    sys.path.insert(0, util)

import ustates, ucalc, ufmt, ulabels, uinit, udb, ukeys

from ucountries import eu_majors
conf = uinit.clargs()

path_to_db = base + '/db/db.max.txt'
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#----------------------------------------

with open(base + '/db/keylists.db.txt') as fh:
    data = fh.read().strip().split('\n\n')

kD = {}

for e in data:
    lines = e.strip().split('\n')
    k = lines.pop(0)
    kD[k] = lines

#-------------------------------

def get_results(conf):

    # the idea here is if there are multiple 'names'
    # then the caller wants them combined into one table
    
    if not conf['names']:
        skL = ukeys.key_list(D)
    elif 'world' in conf['names']:
        skL = ukeys.key_list(D)
        conf['names'].remove('world')
    else:
        skL = []
        
    
    # only countries, no states or counties
    skL = [k for k in skL if k.startswith(';;;')]
    
    
    for name in conf['names']:
        if name == 'eu':
            eu_keys = [';;;' + c for c in eu_majors]
            skL.extend(eu_keys)
            
        elif name == 'counties':
            skL = ukeys.key_list_for_us_counties(D)
            
        # any country w/o states will not be in keylists.db.txt
        elif not name in kD:
            skL.append(';;;' + name)
        
        # otherwise it is
        else:
            if conf['only']:
                skL.append(kD[name][0])
            else:
                skL.extend(kD[name][1:]) 
        
    rL = [D[k][conf['mode']] for k in skL]   
    skL, rL = ucalc.calc(skL, rL, conf)   
    labels,pL = ulabels.assemble(skL, rL, conf)
    
    #-------------------------------
    
    return ufmt.fmt(labels, pL, conf)

if __name__ == "__main__":

    text = get_results(conf)

    if not conf['quiet']:
        print(text)
