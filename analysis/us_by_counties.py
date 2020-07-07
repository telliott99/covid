import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys, ucalc, ufmt

conf = uinit.clargs()
mode = conf['mode']

if conf['all']:
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

conf['regions'] = 'counties'
conf['show_state'] = True

kL, rL = ucalc.calc(kL, rL, conf)
text = ufmt.assemble(kL, rL, conf) 
print(text)
print('')
