import sys, os
from operator import itemgetter

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.udates as udates
import myutil.udb as udb
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath
import myutil.ustrings as ustrings

conf = uinit.clargs()
mode = conf['mode']
n = conf['n']  # num of days of data
N = conf['N']  # num of items

specific_state =conf['arg']

date_info, D = udb.load_db(db='db.txt')
first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

all_dates = udates.generate_dates(first)


#key_info, D = udb.load_db(db='db.txt')
L = []

kL = ukeys.key_list_for_us_counties()

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

def fmt(e):
    c,s,rL,stat = e
    if c == 'Dukes and Nantucket':
        s = 'MA'
    
    v = c + ', ' + s
    pL = [v.ljust(28)]
    pL.append(format(stat,'.2f').rjust(5))
    pL.append(' '.join([str(n).rjust(4) for n in rL]))
    return ' '.join(pL)


dL = udates.slash_dates(all_dates[-n:])
s = 'county                   statistic'.ljust(31)
print(s + ' ' + ' '.join(dL))

L.sort(key=itemgetter(3),reverse = True)

states = []
for e in L[:N]:
    states.append(e[1])
    print(fmt(e))
print()

pL = list()
for state in list(set(states)):
    pL.append((state, states.count(state)))
    pL.sort(key=itemgetter(1),reverse = True)

if not specific_state:   
    for state, count in pL:
        print(state.ljust(15), count)
