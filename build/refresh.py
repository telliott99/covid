import sys, os
import subprocess

#import util as ut
#from util_path import util as ut
sys.path.insert(0,'/Users/telliott/Dropbox/covid')

import myutil.udb as udb
import myutil.udates as udates

# downloads

dL = udb.list_directory(udb.src)
dL = [e.split('.')[0] for e in dL]

rL = []
for d in udates.all_dates:
    if not d in dL:
        rL.append(d.split('-',1)[1])

for arg in rL:
    print "asking to download", arg
    subprocess.call(['python', "fetch.py", arg])
