import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys
import umath, ucalc, ufmt, upop, ustates

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

#---------------------------------------

def entries_for_country(country):
    if country == 'US':
        kL = ustates.key_list_for_states()
    else:
        kL = ukeys.key_list_for_search_term(
            D,country, mode="country")
        
    kL = sorted(kL, key=ukeys.custom_key)
    
    if len(kL) > 1:
        if kL[0][:3] == ';;;':
            kL.pop(0)  
    
    rL = [D[k][conf['mode']] for k in kL]
    return rL, kL

if __name__ == "__main__":

    if not conf['names']:
        print('please supply the name of a country')
        sys.exit() 

    conf['regions'] = 'one_country'

    for country in conf['names']:
        rL,kL = entries_for_country(country)
        kL, rL = ucalc.calc(kL,rL,conf)
        
        if len(rL) == 1:
            conf['totals'] = False
        text = ufmt.assemble(kL, rL, conf)
        print(text)
