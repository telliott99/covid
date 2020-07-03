import sys, os, subprocess
base = os.environ.get('covid_base')
sys.path.insert(0,base)

from do_imports import *

conf = uinit.clargs()
mode = conf['mode']

#---------------------------------------

if not conf['arg']:
    print('please supply the name of a state')
    sys.exit()
    
state = conf['arg']

if conf['max']:
    path_to_db = base + '/db.max.txt'
else:
    path_to_db = base + '/db.txt'
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

# -----------
        
kL = ukeys.key_list_for_search_term(D, state, mode="state")
kL = sorted(kL, key=ukeys.custom_key)

rL = [D[k][conf['mode']] for k in kL]

# -----------

conf['regions'] = 'counties'
print(ufmt.fmt(rL,kL,conf))
