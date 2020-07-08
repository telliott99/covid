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

def go():
    print('please supply the name of a US state')
    sys.exit()

if not conf['names']:
    go()

L = conf['names']

for name in L:
    if not name in ustates.states:
        go()
    
# -----------

for state in L:
    kL = ukeys.key_list_for_search_term(D, state, mode="state")
    
    if conf['total_only']:
        kL = kL[:1]
        assert kL[0].startswith(';')

    else:
        kL = kL[1:]
        kL = sorted(kL, key=ukeys.custom_key)
    
    rL = [D[k][conf['mode']] for k in kL]
    
    if conf['total_only']:
        conf['regions'] = 'states'
    else:
        conf['regions'] = 'counties'

    kL, rL = ucalc.calc(kL, rL, conf)
    text = ufmt.assemble(kL, rL, conf)
    
    # new
    fips = ustates.state_to_fips[state]
    sk = ';'.join(['', state, fips, 'US'])
    
    if not conf['rate'] and not conf['pop'] and not conf['total_only']:
        if not conf['delta']:
            assert conf['totals_line'] == D[sk][mode][-n:]
    
    if not conf['quiet']:
        print(text)
        print('')
    
