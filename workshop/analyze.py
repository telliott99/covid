import sys, os, subprocess
base = os.environ.get('covid_base')
sys.path.insert(0,base)

from do_imports import *

conf = uinit.clargs()
mode = conf['mode']

path_to_db = base + '/db.txt'  
date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#---------------------------------------

if not conf['names']:
    print('please supply the name(s) of one or more states or countries')
    sys.exit()

# sublist for each name
big_list = ukeys.key_list_for_names(D, conf)

# -----------

for kL, region_type in big_list:
    # do each argument separately
    rL = [D[k][conf['mode']] for k in kL] 
    conf['region_type'] = region_type

    text, labels, rL, conf = ufmt.fmt(rL,kL,conf)
    print(text)
    print('')
    
    #if conf['graph']:
        #gL.append(conf['totals_values'])

#if conf['graph']:
    #uplot.plot(gL)