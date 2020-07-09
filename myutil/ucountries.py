import sys, os
base = os.environ.get('covid_base')

if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import udb, udates, umath

eu_majors = [
    'Austria', 
    'Belgium', 
    'Czechia', 
    'Denmark',
    'Estonia',
    'Finland', 
    'France', 
    'Germany', 
    'Greece', 
    'Hungary', 
    'Ireland',
    'Italy', 
    'Latvia', 
    'Lithuania',
    'Netherlands', 
    'Poland', 
    'Portugal', 
    'Spain', 
    'Sweden']

countries_with_states = [
'Australia', 
'Brazil', 
'Canada',
'Chile', 
'China',
'Colombia',
'France',
'Germany', 
'India', 
'Italy', 
'Mexico', 
'Japan', 
'Pakistan',
'Peru', 
'Russia',
'Sweden',
'Spain',
'United Kingdom' ]
