import sys, os, time
import subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

print(os.getcwd())

pre = 'map/'
prog = ['python3']

script_list = ['one_state_map.py',
               'all_states_map.py' ]
               
arg_list = [['CA', 'MN', 'SC', 'TX'],
            [] ]

errors = []

for script, args in zip(script_list, arg_list):
    cmds = prog + [pre + script] + args
    print('running: ' + ' '.join(cmds))
    r = subprocess.run(cmds)
    if (r.returncode != 0):
        errors.append(script)
    print()
    time.sleep(2)

for e in errors:
    print('error code returned for: %s' % e)
  
if not errors:
    print('no errors')
    
subprocess.run(['osascript', '-e' 'quit app "Safari"'])