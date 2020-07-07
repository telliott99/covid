import sys, os
base = os.environ.get('covid_base')

if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys, umath, ucalc, ufmt
import upop, ucountries

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

from country import entries_for_country

def do_eu():
    eu = ucountries.eu_majors
    pL = []
    for c in eu:
        kL = ukeys.key_list_for_search_term(
                 D, c, mode="country")
                 
        # countries with states now have a total
        # that entry comes first  
        k = kL[0]
        assert k[:3] == ';;;'
        vL = D[k][conf['mode']]
        pL.append(vL)
    
    return eu,pL

if __name__ == "__main__":

    kL,rL = do_eu()
    conf['regions'] = 'eu'
    
    kL, rL = ucalc.calc(kL, rL, conf)
    text = ufmt.assemble(kL, rL, conf, do_labels = False) 
    print(text)
    print('')

