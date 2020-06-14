import sys, os, subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

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
