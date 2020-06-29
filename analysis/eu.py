import sys, os, subprocess
base = os.environ.get('covid_base')
sys.path.insert(0,base)

# u___ names available from here:
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

from country import entries_for_country

def do_eu():
    eu = ['Belgium','Czechia','Denmark',
          'Estonia',
          'Germany','Greece','Italy',
          'Latvia','Lithuania','Netherlands',
          'Spain',
          'Poland','Portugal']
    pL = []
    for c in eu:
        rL, ignore = entries_for_country(c)
        pL.append(umath.totals(rL))
    return pL, eu

if __name__ == "__main__":

    pL,labels = do_eu()
    # totals put on in fmt
    print(ufmt.fmt(pL,labels,conf))
    print(len(umath.totals(pL)))