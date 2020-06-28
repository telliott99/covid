import sys, os
import subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

pre = 'geo/'
prog = ['python3']

script_list = ['one_state_map.py',
               'united_states_map.py' ]
arg_list = [['SC', 'TX'],
            [] ]

errors = []

for script, args in zip(script_list, arg_list):
    cmds = prog + [pre + script] + args
    print('running: ' + ' '.join(cmds))
    r = subprocess.run(cmds)
    if (r.returncode != 0):
        errors.append(script)
    print()

for e in errors:
    print('error code returned for: %s' % e)