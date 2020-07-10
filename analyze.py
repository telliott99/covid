import sys, os
base = os.environ.get('covid_base')
sys.path = [base, base + '/myutil'] + sys.path

from uall import sep, calc, assemble, ukeys
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
text = assemble(skL, rL, conf)

if not conf['quiet']:
    print(text)
    print('')


