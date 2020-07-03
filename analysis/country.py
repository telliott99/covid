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

#---------------------------------------

def entries_for_country(country):
    kL = ukeys.key_list_for_search_term(
        D,country, mode="country")
    kL = sorted(kL, key=ukeys.custom_key) 
    rL = [D[k][conf['mode']] for k in kL]
    return rL, kL

if __name__ == "__main__":
    if not conf['arg']:
        print('please supply the name of a country')
        sys.exit()
        
    if conf['pop']:
        print('population normalization not yet implemented for this script')
        sys.exit()
        
    country = conf['arg']
    conf['regions'] = 'countries'

    rL,kL = entries_for_country(country)
    conf['regions'] = 'one_country'
    print(ufmt.fmt(rL,kL,conf))