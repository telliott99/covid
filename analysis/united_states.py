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


if __name__ == "__main__":

    kL = [';;;US']
    conf['regions'] = 'one_country'
    rL = [D[k][mode] for k in kL]
    
    kL, rL = ucalc.calc(kL, rL, conf)

    text = ufmt.assemble(kL, rL, conf, 
                         is_key_list = True) 
                         
                         
    if not conf['quiet']:
        print(text)
        print('')

