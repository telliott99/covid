import sys, os
base = os.environ.get('covid_base')
sys.path = [base, base + '/myutil'] + sys.path

from uall import sep, calc, assemble, ukeys, ufmt
from uall import pprint, kL, conf, D

import ustates
from ucountries import eu_majors

with open(base + '/keylists.db.txt') as fh:
    data = fh.read().strip().split('\n\n')

kD = {}

for e in data:
    lines = e.strip().split('\n')
    k = lines.pop(0)
    kD[k] = lines

#-------------------------------

eu_keys = [';;;' + c for c in eu_majors]

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
        skL.extend(eu_keys)
        
    elif name == 'counties':
        skL = ukeys.key_list_for_us_counties(D)
        
    # any country w/o states is not in keylists.db.txt
    elif not name in kD:
        skL.append(';;;' + name)
        
    elif name == 'US':
        tmp = kD[name]
        if conf['only']:
            skL.append(tmp[0])
            
        else:
            skL.extend(tmp[1:])   
                        
    elif name in ustates.states:
        tmp = kD[name]
        
        if conf['only']:
            skL.append(tmp[0])
        else:
            skL.extend(tmp[1:]) 
    
    else:          
        tmp = kD[name]
        # country with states
        if conf['only']:
            skL.append(tmp[0])
        else:
            skL.extend(tmp[1:])  

rL = [D[k][conf['mode']] for k in skL]   
skL, rL = calc(skL, rL, conf)   
labels,pL = assemble(skL, rL, conf)


#-------------------------------

# formatting as desired

if conf['quiet']:
    sys.exit()

# format for screen
if not conf['csv']:
    extra = 1
    m = max([len(e) for e in labels])
    labels = [e.ljust(m + extra) for e in labels]
    
    n = 0
    for vL in pL:
        # don't count the last value if stats
        if conf['rate']:
            for e in vL[:-1]:
                if len(e) > n:
                    n = len(e)
        else:
            for e in vL:
                if len(e) > n:
                    n = len(e)
    tmp = []
    for vL in pL:
        vL = [e.rjust(n + extra) for e in vL]
        tmp.append(''.join(vL))
    pL = tmp
    
    for l,v in zip(labels,pL):
        print(l + v)

# format csv
else:
    for l,vL in zip(labels,pL):
        print(l + ',' + ','.join(vL))
    

