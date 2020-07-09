import sys, os
base = os.environ.get('covid_base')
sys.path = [base, base + '/myutil'] + sys.path

import ucalc, udates, udb, ufmt 
import uinit, ukeys, umath, upop
import ustates

from udb import sep

calc = ucalc.calc
assemble = ufmt.assemble
pprint = ufmt.pprint

conf = uinit.clargs()
verbose = conf['verbose']

if conf['names'] == []:
    print('please supply a search term')
    print('the name of a US state or a country or eu')
    sys.exit()

mode = conf['mode']

if conf['all']:
    path_to_db = base + '/db.max.txt'
else:
    path_to_db = base + '/db.txt'
    
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

kL = ukeys.key_list(D)

