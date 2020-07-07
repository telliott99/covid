import sys, os

base = os.environ.get('covid_base')
sys.path = [base, base + '/myutil'] + sys.path

import uinit, udb, ukeys

path_to_db = base + '/db.txt'  
date_info, D = udb.load_db(path_to_db)

conf = uinit.clargs()

if not conf['names']:
    print('please supply the name(s) of one or more states or countries')
    uinit.bail()

#---------------------------------------

def get_key_indices(kL, mode = 'state'):
    if mode == 'country':
        f = ukeys.country_for_key
    else: 
        f = ukeys.state_country_for_key
        
    kD = {}
    i = 0
    j = i
    while i < len(kL):
        which = f(kL[i])
        while f(kL[j]) == which:
            j += 1
            if j == len(kL):
                break
        kD[which] = (i,j-1)
        i = j
    return kD
    
kL = ukeys.key_list(D)

db_state_keys = get_key_indices(
    kL, mode = 'state')
db_country_keys = get_key_indices(
    kL, mode = 'country')

#---------------------------------------

def test():
    t = db_country_keys['Germany']
    ckL = kL[t[0]:t[1] + 1]
    print(ckL[0])     
    print(ckL[-1])
    
    t = db_state_keys['Alabama, US']
    skL = kL[t[0]:t[1] + 1]
    print(skL)

if __name__ == "__main__":
    test()



