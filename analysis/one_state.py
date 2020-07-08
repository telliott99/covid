import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys, ucalc, ufmt, ukeys
import ustates

conf = uinit.clargs()
mode = conf['mode']

path_to_db = base + '/db.txt'  
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last
n = conf['n']

#---------------------------------------

if not conf['names']:
    print('please supply the name of a state')
    sys.exit()
    
L = conf['names']

# -----------
gL = []

for state in L:
    kL = ukeys.key_list_for_search_term(D, state, mode="state")
    
    # new
    kL = [k for k in kL if not ukeys.county_for_key(k) == '']
    
    kL = sorted(kL, key=ukeys.custom_key)
    rL = [D[k][conf['mode']] for k in kL]
    
    conf['regions'] = 'counties'

    kL, rL = ucalc.calc(kL, rL, conf)
    text = ufmt.assemble(kL, rL, conf)
    
    # new
    fips = ustates.state_to_fips[state]
    sk = ';'.join(['', state, fips, 'US'])
    
    if not conf['rate'] and not conf['pop']:
        if not conf['delta']:
            assert conf['totals_values'] == D[sk][mode][-n:]
    
    if not conf['quiet']:
        print(text)
        print('')
    
