# these fixes only apply to early days
import sys, os
MX = '--max' in sys.argv

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')
    
import ustrings, udb, ukeys, ustates
import umath

from ukeys import state_for_key
from ustates import state_to_abbrev, abbrev_to_fips

sep = ustrings.sep      # ;

if MX:
    path_to_db = base + '/' + 'db.max.txt'
else:
    path_to_db = base + '/' + 'db.txt'

date_info, D = udb.load_db(path_to_db)
first,last = date_info.split('\n')

#-------------------------------------

kL = ukeys.key_list(D)
additions = {}

def do_us_states():
    for state in ustates.states:
        skL = [k for k in kL if state_for_key(k) == state]
        cases_list = [D[k]['cases'] for k in skL]
        deaths_list = [D[k]['deaths'] for k in skL]
        
        cases = umath.totals(cases_list)
        deaths = umath.totals(deaths_list)
        
        abbrev = state_to_abbrev[state]
        fips = abbrev_to_fips[abbrev]
        
        k = ';'.join(['', state, fips, 'US'])
        sD = {'cases': cases, 'deaths': deaths }
        additions[k] = sD

do_us_states()

def do_country_total(country):
    # at this point, only US states in additions
    cases_list = []
    deaths_list = []
    
    if country == 'US':
        # rather than total the whole db
        # use new state totals
        for k in additions:
            cases_list.append(additions[k]['cases'])
            deaths_list.append(additions[k]['deaths'])
            
    else:
        ckL = [k for k in kL if k.endswith(';' + country)]
        if len(ckL) == 1:
            return
            
        for k in ckL:
            cases_list.append(D[k]['cases'])
            deaths_list.append(D[k]['deaths'])
            
    cases = umath.totals(cases_list)
    deaths = umath.totals(deaths_list)
    
    sD = {'cases': cases, 'deaths':deaths}
    k = ';;;' + country
    additions[k] = sD
    

others = ['Australia', 'Canada',
          'Germany', 'Italy', 
          'France', 'Sweden',
          'Spain',
          'United Kingdom',
          'Japan', 'China',
          'Mexico', 
          'Brazil', 'Chile', 
          'Peru', 'Colombia',
          'India', 'Pakistan' ]
         

for c in ['US'] + others:
    do_country_total(c)

for k in additions:
    D[k] = additions[k]

udb.save_db(D, path_to_db, first, last)




