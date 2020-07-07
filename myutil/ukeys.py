import sys, os

import sys, os
base = os.environ.get('covid_base')

if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import ustrings, umath, ustates, udb

def state_for_key(k):
    county,state,fips,country = k.split(ustrings.sep)
    return state
    
def fips_for_key(k):
    county,state,fips,country = k.split(ustrings.sep)
    return fips

def county_for_key(k):
    county,state,fips,country = k.split(ustrings.sep)
    return county

def custom_key(s):
    L = s.split(ustrings.sep)
    return L[3], L[1], L[0], L[2]
    
def build_key_for_state(state):
    try:
        abbrev = ustates.state_to_abbrev[state]
    except KeyError:
        assert state in ustates.terr
        abbrev = ustates.terr_to_abbrev[state]
    fips = ustates.abbrev_to_fips[abbrev]
    return udb.sep.join(['',state,fips,'US'])

#----------------------------------

def key_list(D):
    return sorted(D.keys(),key=custom_key)
    
def key_list_for_names(D, conf):
    L = conf['names']
    ret = []
    big_list = key_list(D)
    
    for s in L:
        kL = [k for k in big_list if k.endswith(';' + s)]
        if kL:
            ret.append((kL, 'country'))
        else:
            mode = 'state'
            kL = key_list_for_search_term(D, 
                s, mode = mode)
            if kL:
                ret.append((kL, mode))
            else:
                mode = 'county'
                kL = key_list_for_search_term(D, 
                s, mode = mode)
                ret.append((kL, mode))
            
    return ret

def key_list_for_search_term(D, s, mode="country"):
    kL = list()
    for k in key_list(D):
        county,state,fips,country = k.split(ustrings.sep)
        if mode == "country" and s == country:
            kL.append(k)
        elif mode == "state" and s == state:
            kL.append(k)
        elif mode == "county" and s == county:
            kL.append(k)
    return kL

def all_states(D):
    # exclude:
    # ;Diamond Princess;88888;US
    # ;Puerto Rico;00072;US

    kL = key_list_for_search_term(D, 'US', mode="country")
    rL = list()
    for k in kL:
        c,s,fips,y = k.split(uts.sep)
        if c == '':
            continue
        if fips != '':
            rL.append(s)
    rL = list(set(rL))
    rL.sort()
    return rL

    
def key_list_for_us_counties(D):
    rL = list()
    for k in key_list(D):
        county,state,fips,country = k.strip().split(ustrings.sep)
        if not country == 'US':
            continue
        if county == '':  # US territory
            continue
        weird = ['unassigned',
                 'Unassigned', 
                 'Unknown',
                 'Federal Correctional Institution (FCI)',
                 'Michigan Department of Corrections (MDOC)']
                 
        if county in weird or county.startswith('Out'):
            continue
        rL.append(k)
    return rL

# mutating
def switch(D, old_key, new_key):
    D[new_key] = D[old_key]
    D.pop(old_key)

#------------------------------------

def merge_keys(D, old, new):
    if not old in D:
        return
    if not new in D:
        D[new] = D[old]
    
    modes = ['cases', 'deaths']
    mD = {}
            
    for m in modes:
        cL1, cL2 = D[old][m],D[new][m]
        try:
            cL = umath.merge(cL1,cL2)
        except AssertionError:
            print('error in merge_keys')
            print(old, len(cL1))
            print(new, len(cL2))
        
        mD[m] = cL
    D[new] = mD

def popif(D,k):
    try:
        D.pop(k)
    except:
        pass
