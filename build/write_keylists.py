# python3 write_keylists.py > keys.db.txt

# keylists contain all keys for a given search term
# like US or South Carolina
# pre-computed and stored as keylists.db.txt

import sys, os

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
myutil = base + '/myutil'
if not myutil in sys.path:
    sys.path.insert(0, myutil)
    
import udb, ucalc, ulabels, ufmt, ukeys
import ustates, ucountries

from ustates import states
from ukeys import build_key_for_state
from ucountries import countries_with_states

path_to_db = base + '/db/db.max.txt'
date_info, D = udb.load_db(path_to_db)

sep = udb.sep

# these are sorted, so it's easy

kL = ukeys.key_list(D)

def keys_for_state(s):
    skL = [k for k in kL if k.split(sep)[1] == s]
    return skL
    
def keys_for_country(c):
    ckL = []
    for k in kL:
        county, state, fips, country = k.split(sep)
        if country == c and county == '':
            ckL.append(k)  
    return ckL

#-------------------------------

pL = []

for state in states:
    pL.append(state)
    skL = keys_for_state(state)
    for e in skL:
        pL.append(e)
    pL.append('')

for country in countries_with_states + ['US']:
    pL.append(country)
    ckL = keys_for_country(country)
    for e in ckL:
        pL.append(e)
    pL.append('')
    
with open(base + '/db/keylists.db.txt', 'w') as fh:
    fh.write('\n'.join(pL))




