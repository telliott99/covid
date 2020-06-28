import sys, os, subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.udates as udates
import myutil.ufile as ufile
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath

#---------------------------------------

conf = uinit.clargs()
#mode = conf['mode']
mode = 'cases'

if not conf['arg']:
    print('please supply the name of a country')
    sys.exit()
    
country = conf['arg']

sep = ustrings.sep      # ;
path_to_db = base + '/db.txt'

date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#---------------------------------------

kL = ukeys.key_list_for_search_term(country, mode="country")
kL = sorted(kL, key=ukeys.custom_key)

rL = [D[k][conf['mode']] for k in kL]

# -----------

labels = []
for k in kL:
    labels.append(k.split(sep)[1] + ', ' + country)
    
print(ufmt.fmt(rL,labels,conf))
