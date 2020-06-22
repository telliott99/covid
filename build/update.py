import sys, os, subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.udates as udates
import myutil.ukeys as ukeys


overwrite = len(sys.argv) > 1
if overwrite:
    print('overwrite db')

sep = ustrings.sep      # ;
sep2 = ustrings.sep2    # #

src = udb.src

all_dates = udates.all_dates
first = all_dates[0]
last = all_dates[-1]

db = udb.db  # db.txt

# we check that csv.source
# is up-to-date and no files are missing

dL = udb.list_directory(src)
fL = [d.split('.')[0] for d in dL]
#print dL

for date in all_dates:
    if not date in fL:
        print('missing data file in ' + src)
        subprocess.call(['python', "refresh.py"])
        
#-----------------

# for constructing the database file
# there is no need to convert to ints
    
def init_db():
    path = 'csv.source' + '/' + first + '.csv'
    print('init db with file:  ', first)
    D = udb.read_csv_data_file(path)        
    
    with open(db, 'w') as fh:
        fh.write(first + '\n')
        fh.write(first + '\n')
        fh.write('\n')
        
        for k in sorted(D.keys(), key=ukeys.custom_key):
            fh.write(k + '\n')
            fh.write(D[k]['cases'] + '\n')
            fh.write(D[k]['deaths'] + '\n')
            fh.write('\n')
    
if not os.path.exists(db) or overwrite:
    init_db()

#----------------------------

date_info, D = udb.load_db()

# find the date of the latest data in the db
last_update = date_info.split('\n')[1]

#----------------------------
    
# add new values

i = all_dates.index(last_update)
all_dates = udates.all_dates[i+1:]

for date in all_dates:
    fn = src + '/' + date + '.csv'
    sD = udb.read_csv_data_file(fn)
    
    for k in sD:
        cases = sD[k]['cases']
        deaths = sD[k]['deaths']
        
        if k in D:
            D[k]['cases'].append(cases)
            D[k]['deaths'].append(deaths)
                            
        else:
            # pad for missing data
            j = all_dates.index(date)
            pad = [0] * j
            D[k] = {}
            D[k]['cases'] =  pad[:] + [cases]
            D[k]['deaths'] = pad[:] + [deaths]

        #if k == 'Cook;Minnesota;27031;US':
            #print(D[k])
    
    # now look for keys with no updates
    for k in D:
        if not k in sD:
            D[k]['cases'].append(0)
            D[k]['deaths'].append(0)

#----------------------------

udb.save_db(D)

subprocess.call(['python', 'fixit.py'])

#subprocess.call(['cp', 'db.txt', '../db.txt'])
