import sys, os

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

path_to_db = base + '/db.txt'

date_info, D = udb.load_db(path_to_db)
first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#-------------------------

kL = [k for k in D if k[-3:] == ';US']
kL = sorted(kL, key=ukeys.custom_key)

kL = [k for k in kL if not 'Princess' in k and not 'Recovered' in k]

# group keys by state in one pass
# kL is already sorted first by state and then by county

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

def test():
    for state in sorted(kD.keys()):
        print(state)
        i,j = kD[state]
        print(i, kL[i])
        print(j, kL[j])
        print()

# test()

#=========================

states = sorted(kD.keys())

filterL = ['Northern Mariana Islands',
           'Puerto Rico',
           'Virgin Islands',
           'Guam' ]
           
states = [name for name in states if not name in filterL]

rL = list()
for state in states:
    # location of first/last index for each county
    i,j = kD[state]
    tmp = [D[k][mode] for k in kL[i:j+1]]
    rL.append(umath.totals(tmp))

#--------------

labels = states

if __name__ == "__main__":
    print(ufmt.fmt(rL,labels,conf))
