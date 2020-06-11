import sys, os

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
state = conf['arg']

date_info, D = udb.load_db()

# -----------
        
kL = ukeys.key_list_for_search_term(state, mode="state")
kL = sorted(kL, cmp=ukeys.custom_sort)

# -----------

labels = []
for k in kL:
    c,s,fips,y = k.strip().split(ustrings.sep)
    labels.append(c)
labels.append('totals')

n_days = n
rL = [D[k][mode][-n_days:] for k in kL]
totals = umath.totals(rL)
rL.append(totals)

# -----------

print s

# a,b are pad lengths for labels, values
a,b,result = ufmt.fmt_screen(labels, rL, num=n_days)

dates = ufmt.fmt_dates(n_days)
dates = ''.join([d.rjust(b) for d in dates])

print 'date'.ljust(a) + dates

print(result)
print
