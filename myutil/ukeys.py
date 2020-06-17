import udb
import ustrings

def state_for_key(k):
    county,state,fips,country = k.split(ustrings.sep)
    return state
    
def fips_for_key(k):
    county,state,fips,country = k.split(ustrings.sep)
    return fips

def county_for_key(k):
    county,state,fips,country = k.split(ustrings.sep)
    return county

'''
# custom sort, by country (US first), then state, county fips
# doesn't work in Python 3

def custom_sort(a,b):
    kL1 = a.split(';')
    kL2 = b.split(';')
    if kL1[3] == 'US':
         if kL2[3] != 'US':
             return -1
    if kL2[3] == 'US':
         if kL1[3] != 'US':
             return 1
    
    for i in (3,1,0):
        r = cmp(kL1[i],kL2[i])
        if r: return r
    return cmp(kL1[1],kL2[1])
'''

def custom_key(s):
    L = s.split(ustrings.sep)
    return L[3], L[1], L[0], L[2]

# key stuff

def key_list(D):
    return sorted(D.keys(),key=custom_key)

def key_list_for_search_term(s,mode="country"):
    rL = list()
    date_info, D = udb.load_db()
    for k in key_list(D):
        county,state,fips,country = k.split(ustrings.sep)
        if mode == "country" and s == country:
            rL.append(k)
        elif mode == "state" and s == state:
            rL.append(k)
        elif mode == "county" and s == county:
            rL.append(k)
    return rL

def all_states():
    # exclude:
    # ;Diamond Princess;88888;US
    # ;Puerto Rico;00072;US

    kL = key_list_for_search_term('US',mode="country")
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

    
def key_list_for_us_counties():
    rL = list()
    date_info, D = udb.load_db()
    for k in key_list(D):
        county,state,fips,country = k.strip().split(ustrings.sep)
        if not country == 'US':
            continue
        if county == '':  # US territory
            continue
        weird = ['unassigned','Unassigned', 'Unknown',
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
