import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, udates, ustates, ukeys
import ustrings, umath

from operator import itemgetter

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

if conf['pop']:
    print('normalization not yet implemented')
    uinit.bail()
    
#-------------------------

n = conf['n']  # num of days of dataå

aL = conf['names']

specific_state = None
if aL:
    specific_state = aL[0]

all_dates = udates.generate_dates(first)


#key_info, D = udb.load_db(db='db.txt')
L = []

kL = ukeys.key_list_for_us_counties(D)

for k in kL:
    c,s,fips,y = k.strip().split(ustrings.sep)
    if specific_state and specific_state != s:
        continue
    
    rL = D[k][mode][-n:]
    if mode == 'cases' and rL[-1] < 40:
        continue
    f = umath.stat(rL)
    if f:
        L.append((c, s, rL, f))

#-----------------

def fmt(e, pad):
    c,s,rL,stat = e
    abbrev = ustates.state_to_abbrev[s]
    
    v = c + ', ' + abbrev
    pL = [v.ljust(pad)]
    pL.append(' '.join([str(n).rjust(6) for n in rL]))
    pL.append(format(stat,'.2f').rjust(5))
    return ' '.join(pL)


L.sort(key=itemgetter(3),reverse = True)

states = []
if conf['N']:     # num of rows
    L = L[:conf['N']]

pad = 0
for t in L:
    m = len(t[0])
    if pad < m:
        pad = m
pad += 4

dL = udates.slash_dates(all_dates[-n:])
s = 'county'.ljust(pad + 3)

print(s + (' '*3).join(dL) + '  statistic')
    
for e in L:
    states.append(e[1])
    print(fmt(e, pad))
    
print('')

#-------------------------
# summary of states with hot counties

pL = list()
for state in list(set(states)):
    pL.append((state, states.count(state)))
    pL.sort(key=itemgetter(1),reverse = True)

if not specific_state:   
    for state, count in pL:
        print(state.ljust(15), count)
