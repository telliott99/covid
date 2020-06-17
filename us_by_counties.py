import sys
from operator import itemgetter

import myutil.udates as udates
import myutil.udb as udb
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath
import myutil.ustrings as ustrings


conf = uinit.clargs()
mode = conf['mode']

date_info, D = udb.load_db()
conf['first'], conf['last'] = date_info.split('\n')

#-------------------------

kL = ukeys.key_list_for_us_counties()
rL = [D[k][mode] for k in kL]

labels = []
for k in kL:
    county = ukeys.county_for_key(k)
    state = ukeys.state_for_key(k)
    labels.append(county + ', ' + state)

print(ufmt.fmt(rL,labels,conf))
