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

def custom_key(s):
    L = s.split(ustrings.sep)
    return L[3], L[1], L[0], L[2]


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
