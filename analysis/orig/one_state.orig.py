import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys, ucalc, ufmt

conf = uinit.clargs()
mode = conf['mode']

path_to_db = base + '/db.txt'  
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last


#---------------------------------------

if not conf['names']:
    print('please supply the name of a state')
    sys.exit()
    
L = conf['names']

# -----------
gL = []

for state in L:
    kL = ukeys.key_list_for_search_term(D, state, mode="state")
    kL = sorted(kL, key=ukeys.custom_key)
    
    rL = [D[k][conf['mode']] for k in kL]
    
    conf['regions'] = 'counties'

    kL, rL = ucalc.calc(kL, rL, conf)
    text = ufmt.assemble(kL, rL, conf) 
    print(text)
    print('')
    
