import sys, os
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
state = conf['arg']
conf['N'] = 100

if not state:
   print 'please enter a state'
   sys.exit()

date_info, D = udb.load_db()

# -----------
        
kL = ukeys.key_list_for_search_term(state, mode="state")
kL = sorted(kL, cmp=ukeys.custom_sort)

labels = []
for k in kL:
    c,s,fips,y = k.strip().split(ustrings.sep)
    labels.append(c)

rL = [D[k][mode] for k in kL]
pL = ufmt.fmt_new(rL,
                 state,
                 labels,
                 conf)

row1 = pL.pop(0)
total = pL.pop()

print row1
pL.sort(key=itemgetter(1),reverse = True)
for s,stat in pL:
    if stat == 'na':
        print s + '  ' + stat
    else:
        print s + '  ' + str(round(stat,3))
print total[0] + '  ' + str(round(total[1],3))

