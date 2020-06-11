# found county population data on the web
# this data is 2019
import sys
import util as ut

# load database

date_info, D = ut.load_db()

#---------------

# load population data

fn = '/Users/telliott/Github/covid/pop/pop.csv'

with open(fn) as fh:
    pop_data = fh.read().strip().split('\n')

pD = {}
for e in pop_data:
    loc,pop = e.split(',')
    pD[loc] = pop
   
#---------------

def test():
    def search(loc):
        for k in D.keys():
            if k.startswith(loc):
                return True
        return False

    for loc in pD:
        if not search(loc):
            print loc, 'not found'

# test()

'''
Dukes and Nantucket;Massachusetts not found
New York;New York not found

that's because 
Dukes, Nantucket are listed separately in Covid db

three counties are combined into NYC:  
New York, Brooklyn, Bronx
'''

n = 0
for loc in ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']:
    n += int(pD[loc + ';New York'])

pD['New York City'] = str(n)

#---------------

def run(D):
    mD = {}
    kL = ut.key_list_for_us_counties()
    for k in kL:
        mD[k] = D[k]
        county,state,fips,country = k.split(ut.sep)
        specials = ['Carson City', 'James City']
        if county.endswith('City') and not county in specials:  
            county = county.replace(' City','')
        if county.endswith('County'):  
            county = county.replace(' County','')
        if county == 'Charles' and state == 'Virginia':
            county = 'Charles City'
        mod = ';'.join([county,state])
        mD[k]['pop'] = pD[mod]
    return mD

if __name__ == "__main__":
    date_info, D = ut.load_db()
    mD = run(D)
    kL = ut.key_list_for_us_counties()
    for k in kL:
        print k, mD[k]['pop']