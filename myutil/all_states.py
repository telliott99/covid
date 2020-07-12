import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udb, ukeys, umath, ucalc, ufmt

conf = uinit.clargs()
v = conf['verbose']

mode = conf['mode']

path_to_db = base + '/db/db.max.txt'

date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#-------------------------

kL = [k for k in D if k[-3:] == ';US']

# new since I've added keys for states and US
#print(D[';Alabama;01;US']['cases'][-7:])
#print(D[';;;US']['cases'][-7:])

kL = [k for k in D if not ukeys.state_for_key(k) == '']
kL = [k for k in D if not ukeys.county_for_key(k) == '']

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
           'Guam',
           'Wuhan Evacuee']
           
states = [name for name in states if not name in filterL]

rL = list()

for state in states:
    # location of first/last index for each county
    i,j = kD[state]
    tmp = [D[k][mode] for k in kL[i:j+1]]
    rL.append(umath.totals(tmp))

#--------------

conf['regions'] = 'states'

from ukeys import build_key_for_state

kL = [build_key_for_state(state) for state in states]

if __name__ == "__main__":

    kL, rL = ucalc.calc(kL, rL, conf)
    text = ufmt.assemble(kL, rL, conf) 
    if not conf['quiet']:
        print(text)
        print('')
