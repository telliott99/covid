import sys
import util as ut
import subprocess

D = ut.clargs()
mode = D['mode']

sL = ut.all_states()

for state in sL:
    if mode == "deaths":
        subprocess.call(
            ['python', "state_by_counties.py", state, '-d'])    
    else:
        subprocess.call(
            ['python', "state_by_counties.py", state])
