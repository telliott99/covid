import sys, os
import subprocess

#import util as ut
#from util_path import util.str as uts
sys.path.insert(0,'/Users/telliott/Dropbox/covid')
import util.strings as uts
import util.db as utdb
import util.dates as dates
import util.keys as utk


overwrite = len(sys.argv) > 1
if overwrite:
    print 'overwrite db'

sep = uts.sep      # ;
sep2 = uts.sep2    # #

src = utdb.src

all_dates = dates.all_dates
first = all_dates[0]
last = all_dates[-1]

db = utdb.db  # db.txt

# we check that csv.source
# is up-to-date and no files are missing

dL = utdb.list_directory(src)
fL = [d.split('.')[0] for d in dL]
#print dL

for date in dates.all_dates:
    if not date in fL:
        print 'missing data file in ' + src
        subprocess.call(['python', "refresh.py"])
        
#-----------------

# for constructing the database file
# there is no need to convert to ints
    
def init_db():
    path = 'csv.source' + '/' + first + '.csv'
    print 'init db with file:  ', first
    D = utdb.read_csv_data_file(path)        
    
    with open(db, 'w') as fh:
        fh.write(first + '\n')
        fh.write(first + '\n')
        fh.write('\n')
        
        for k in sorted(D.keys(), cmp=utk.custom_sort):
            fh.write(k + '\n')
            fh.write(D[k]['cases'] + '\n')
            fh.write(D[k]['deaths'] + '\n')
            fh.write('\n')
    
if not os.path.exists(db) or overwrite:
    init_db()

#----------------------------

date_info, D = utdb.load_db()

# find the date of the latest data in the db
last_update = date_info.split('\n')[1]

#----------------------------
    
# add new values

i = all_dates.index(last_update)
all_dates = all_dates[i+1:]

for date in all_dates:
    fn = src + '/' + date + '.csv'
    sD = utdb.read_csv_data_file(fn)
    
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
    
    # now look for keys with no updates
    for k in D:
        if not k in sD:
            D[k]['cases'].append(0)
            D[k]['deaths'].append(0)

#----------------------------

utdb.save_db(D)

