import sys, os

import myutil.udates as udates
import myutil.udb as udb
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath
import myutil.ustrings as ustrings


conf = uinit.clargs()
mode = conf['mode']

if not conf['arg']:
    print('please supply the name of a state')
    sys.exit()
    
state = conf['arg']

date_info, D = udb.load_db()

from ustrings import us_states
rD = {}
for k in us_states:
    rD[us_states[k]] = k

if not state in us_states:  # spelled out
    if state in rD:
        state = rD[state]

# -----------
        
kL = ukeys.key_list_for_search_term(state, mode="state")
kL = sorted(kL, key=ukeys.custom_key)

rL = [D[k][conf['mode']] for k in kL]

# -----------

labels = []
for k in kL:
    labels.append(ukeys.county_for_key(k))
    
print(ufmt.fmt(rL,labels,conf))
