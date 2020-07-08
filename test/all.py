import sys, os
import subprocess

if sys.version_info[0] < 3:
    print('use python3 for this script')
    sys.exit()

base = os.environ.get('covid_base')
sys.path.insert(0,base)

pre = 'analysis/'
prog = ['python3']

errors = []

cmds = prog + [pre + 'all_states.py', '-q']
for arg in 'acprstw':
    print('running: ' + ' '.join(cmds + ['-' + arg]))
    r = subprocess.run(cmds + ['-' + arg])
    if (r.returncode != 0):
        errors.append(script)
    
D = {
      'all_states.py':     ['-c'],
      'all_states.py':     ['-rs', '-N', '3'],
      'one_state.py':      ['HI', '-rs'],
      'one_state.py':      ['SC', '-N', '3'],
      'us_by_counties.py': ['-rs', '-N', '3'],
      
      'trends.py':         ['-n','4', '-N', '3'],
      'country.py':        ['Mexico', '-c', '-N', '3'],
      'country.py':        ['Switzerland'],
      'eu.py':             ['-N', '3'],
      'country.py':        ['Russia', '-p', '-q']
    
    }
      
for script in D:
    args = D[script]
    cmds = prog + [pre + script] + args
    print('running: ')
    print(' '.join(cmds))
    
    r = subprocess.run(cmds)
    if (r.returncode != 0):
        errors.append(script)
    print()

for e in errors:
    print('error code returned for: %s' % e)

if not errors:
    print('no errors')