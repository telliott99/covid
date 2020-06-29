import sys, os, subprocess
base = os.environ.get('covid_base')
sys.path.insert(0,base)

from do_imports import *

conf = uinit.clargs()
mode = conf['mode']

if conf['max']:
    path_to_db = base + '/db.max.txt'
else:
    path_to_db = base + '/db.txt'
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#-------------------------

kL = ukeys.key_list_for_us_counties(D)
rL = [D[k][mode] for k in kL]

labels = []
for k in kL:
    county = ukeys.county_for_key(k)
    state = ukeys.state_for_key(k)
    abbrev = ustrings.state_to_abbrev[state]
    labels.append(county + ', ' + abbrev)

print(ufmt.fmt(rL,labels,conf))
