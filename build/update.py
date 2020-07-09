import sys, os, subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import uinit, udates
import udb, ufile, ukeys, ufmt
from ufmt import pprint

conf = uinit.clargs()
MX = conf['all']

sep = udb.sep      # ;
sep2 = udb.sep2    # #

src = base + '/build/csv.source'

if MX:
    path_to_db = base + '/db.max.txt'
    
else:
    path_to_db = base + '/db.txt'
        
#-----------------
  
if MX:  
    fL = []
    todo = []
    
    def process_dir(d):
        dL = os.listdir(d)
        for fn in dL:
            if fn.startswith('.'):
                continue
            p = d + '/' + fn
            if os.path.isdir(p):
                todo.append(p)
            else:
                fL.append(p)
            
    process_dir(src)

    while todo:
        next = todo.pop()
        process_dir(next)

else:
    # filter out directories
    fL = ufile.list_directory(src)
    fL = [src + '/' + fn for fn in fL]

# fL has full paths
fL.sort(key = udates.date_from_path)

#-----------------

if MX:
    first = '2020-03-22'
else:
    first = udates.date_from_path(fL[0])
    
all_dates = udates.generate_dates(first=first)
last = all_dates[-1]

#-----------------

# for standard build, check that csv.source
# is up-to-date and no files are missing
# can't do that for MX without more logic

if not MX:
    # files present as dates
    dL = [udates.date_from_path(p) for p in fL]
    
    for date in all_dates:
        if not date in dL:
            print('missing data', date)
            subprocess.call(['python', "fetch.py", src, date])

#=================

# for constructing the database file
# there is no need to convert to ints
    
def init_db(path_to_db):
    path = fL[0]
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
    
#if not os.path.exists(db) or overwrite:
init_db(path_to_db)

#----------------------------

date_info, D = udb.load_db(path_to_db)

'''
pad for missing data is confusing 
when we're just updating

for now, build always
(ignore overwrite flag)
'''

# latest update
#t = date_info.split('\n')
#assert first == t[0]
#latest_update = t[1]

delta = 0
    
for fn in fL[1:]:
    delta += 1
    sD = udb.read_csv_data_file(fn)
    date = udates.date_from_path(fn)
    
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


if MX:
    subprocess.call(['python3', 'easy_fixes.py', '--all'])
    subprocess.call(['python3', 'totals.py', '--all'])
    
else:
    subprocess.call(['python3', 'easy_fixes.py' ])
    subprocess.call(['python3', 'totals.py' ])

subprocess.call(['python3', 'write_keylists.py', '>', 'keylists.db.txt' ])

