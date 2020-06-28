import sys, os
import subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

#subprocess.call(['python', 'scripts/all_states.py'])

pre = 'scripts/'
prog = ['python3']

script_list = ['all_states.py',
               'one_state.py',
               'us_by_counties.py',
               'trends.py' ]
arg_list = [[],
            ['SC', '-rs'],
            ['-d'],
            []]

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