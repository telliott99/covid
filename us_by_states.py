import sys
from operator import itemgetter

import myutil.udates as udates
import myutil.udb as udb
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath
import myutil.ustrings as ustrings


conf = uinit.clargs()
mode = conf['mode']
date_info, D = udb.load_db()

#--------------

kL = [k for k in D if k[-3:] == ';US']
kL = sorted(kL, cmp=ukeys.custom_sort)
kL = [k for k in kL if not 'Princess' in k and not 'Recovered' in k]

kD = {}
i = 0
j = i

while i < len(kL):
    which = ukeys.state_for_key(kL[i])
    while ukeys.state_for_key(kL[j]) == which:
        j += 1
        if j == len(kL):
            break
            
    kD[which] = (i,j-1)
    i = j

#--------------
states = sorted(kD.keys())

filterL = ['Northern Mariana Islands',
           'Puerto Rico',
           'Virgin Islands',
           'Guam' ]
           
states = [name for name in states if not name in filterL]

rL = []
n = conf['n']

rL = list()
for state in states:
    i,j = kD[state]  # location of index for each county
    tmp = [D[k][mode][-n:] for k in kL[i:j+1]]
    rL.append(umath.totals(tmp))

stats = [umath.stat(sL) for sL in rL]

pL = ufmt.fmt_new(rL,states,conf)

tL = zip(pL,stats)
tL.sort(key=itemgetter(1), reverse=True)

for s,st in tL[:conf['N']]:
    print s, "  %s" % str(round(st,3))
    
'''
for state in sorted(kD.keys()):
    print state
    i,j = kD[state]
    print i, kL[i]
    print j, kL[j]
    print 
'''