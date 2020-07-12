# for now, removed logic to build smaller db

import sys, os, subprocess

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
util = base + '/myutil'
if not util in sys.path:
    sys.path.insert(0, util)

import uinit, udates
import udb, ufile, ukeys, ufmt
import update_src

from ufmt import pprint

conf = uinit.clargs()

sep = udb.sep      # ;
sep2 = udb.sep2    # #

src = base + '/build/csv.source'
path_to_db = base + '/db/db.max.txt'

#-------------------------------------

# fetch any missing files

update_src.run(src)

fL = update_src.list_src_all(src)
first = '2020-03-22'
    
all_dates = udates.generate_dates(first=first)
last = all_dates[-1]

print('first: ', first, 'last:', last)

#-------------------------------------

# for constructing the database file
# there is no need to convert to ints
    
def init_db(path_to_db):
    fn = fL[0]
    path = src + '/' + fn
    print('init w/:  ', path)
    
    D = udb.read_csv_data_file(path)        
    
    with open(path_to_db, 'w') as fh:
        # write date_info
        fh.write(first + '\n')
        fh.write(first + '\n')
        fh.write('\n')
        
        for k in sorted(D.keys(), key=ukeys.custom_key):
        
            fh.write(k + '\n')
            fh.write(D[k]['cases'] + '\n')
            fh.write(D[k]['deaths'] + '\n')
            fh.write('\n')

# we don't do this anymore:
# if not os.path.exists(db) or overwrite:

init_db(path_to_db)

#----------------------------

date_info, D = udb.load_db(path_to_db)

'''
pad for missing data is confusing 
when we're just updating

for now, build always
(ignore overwrite flag)
'''

delta = 0
    
for fn in fL[1:]:
    delta += 1
    path = src + '/' + fn
    sD = udb.read_csv_data_file(path)
    date = udates.date_from_path(path)
    
    for k in sD:
    
        cases = sD[k]['cases']
        deaths = sD[k]['deaths']
        
        if k in D:
            D[k]['cases'].append(cases)
            D[k]['deaths'].append(deaths)
                            
        else:
            # pad for missing data
            # j = all_dates.index(date)
            print('%s, add key: %s' % (date,k))            
            pad = [0] * delta
            D[k] = {}
            D[k]['cases'] =  pad[:] + [cases]
            D[k]['deaths'] = pad[:] + [deaths]
            
    # now look for keys with no updates
    for k in D:
        if not k in sD:
            #D[k]['cases'].append(0)
            #D[k]['deaths'].append(0)
            x = D[k]['cases'][-1]
            D[k]['cases'].append(x)
            x = D[k]['deaths'][-1]
            D[k]['deaths'].append(x)
           
#----------------------------

print('write: %s' % path_to_db)
udb.save_db(D, path_to_db, first, last)


subprocess.call(['python3', 'easy_fixes.py' ])
subprocess.call(['python3', 'totals.py' ])
subprocess.call(['python3', 'write_keylists.py', '>', 'keylists.db.txt' ])
