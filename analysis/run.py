import sys, os
base = os.environ.get('covid_base')
sys.path = [base, base + '/myutil'] + sys.path

from uall import sep, calc, assemble
from uall import pprint, kL, conf, D

import ustates
from ucountries import eu_majors

with open(base + '/keylists.db.txt') as fh:
    data = fh.read().strip().split('\n\n')

kD = {}

for e in data:
    lines = e.strip().split('\n')
    k = lines.pop(0)
    kD[k] = lines

#-------------------------------

s = '''
;;;Austria
;;;Belgium
;;;Czechia
;;;Denmark
;;;Estonia
;;;Finland
;;;France
;;;Germany
;;;Greece
;;;Hungary
;;;Ireland
;;;Italy
;;;Latvia
;;;Lithuania
;;;Netherlands
;;;Poland
;;;Portugal
;;;Spain
;;;Sweden
'''

eu = s.strip().split('\n')


def get_key_list(name, conf):

    if name == 'eu':
        skL = eu[:]
        conf['key_list_type'] = 'country'
        conf['add_totals'] = True
        return skL, conf

    # any country w/o states is not in keylists.db.txt
    if not name in kD:
        #print(name, 'not in keylists.db.txt')
        skL = [';;;' + name]
        conf['key_list_type'] = 'country'
        conf['only'] = True
        conf['add_totals'] = False
        return skL, conf
    
    # all names in kD from this point

    if name == 'US':
        skL = kD[name]
        if conf['only']:
            #print(name, 'only')
            skL = skL[:1]
            conf['key_list_type'] = 'country'
            conf['add_totals'] = False
            return skL, conf
        else:
            #print(name, 'states')
            skL = skL[1:]
            conf['key_list_type'] = 'state'
            return skL, conf
            
    if name in ustates.states:
        skL = kD[name]
        if conf['only']:
            #print(name, 'a US state')
            skL = skL[:1]
            conf['key_list_type'] = 'state'
            conf['add_totals'] = False
            return skL, conf
        else:
            #print(name, 'a US state, plus counties')
            skL = skL[1:]
            conf['show_state_label'] = True
            conf['key_list_type'] = 'county'
            return skL, conf

    # country with states
    skL = kD[name]
    if conf['only']:
        #print(name, 'a country')
        skL = skL[:1]
        conf['key_list_type'] = 'country'
        conf['add_totals'] = False
        return skL, conf  
    else:
        #print(name, 'a country with states')
        skL = skL[1:]
        conf['show_state_label'] = True
        conf['key_list_type'] = 'state'
        return skL, conf


def do_key_list(skL, conf):    
    rL = [D[k][conf['mode']] for k in skL]   
    skL, rL = calc(skL, rL, conf)   
    return assemble(skL, rL, conf)

#-----------------------------------
            
for name in conf['names']:
    skL, conf = get_key_list(name, conf) 
    text = do_key_list(skL, conf)
    
    if not conf['quiet']:
        print(text)
        print('')

