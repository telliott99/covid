import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys, umath, ucalc, ufmt, ustates
from usearch import db_state_keys, db_country_keys

conf = uinit.clargs()
v = conf['verbose']

mode = conf['mode']

if conf['all']:
    path_to_db = base + '/db.max.txt'
else:
    path_to_db = base + '/db.txt'
date_info, D = udb.load_db(path_to_db)
kL = ukeys.key_list(D)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#-------------------------

# counties only for US states and territories

def get_keys(s):
    if s == 'US':
        pass
    elif s in ustates.states:
        # prevent name conflicts with ', US'
        t = db_state_keys[s + ', US']
        skL = kL[t[0]:t[1]]
    else:
        t = db_country_keys[s]
        skL = kL[t[0]:t[1]]
        if not skL:
            skL = ukeys.key_list_for_search_term(D,s)
    return skL
        
for name in conf['names']:
    skL = get_keys(name)
    for k in skL:
        print(k)
