import sys, os

base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(0,base + '/population')

import myutil.udb as udb
import myutil.ukeys as ukeys
import myutil.ustrings as ustrings

date_info, D = udb.load_db()

#---------------

def test():
    pD = udb.get_popD()
    kL = ukeys.key_list_for_us_counties()
    
    for k in kL:
        county, state, fips, country = k.split(ustrings.sep)
        cs = county + ', ' + state
        if not cs in pD:
             print cs
    
if __name__ == "__main__":
    test()