import sys, os
import subprocess

if sys.version_info[0] < 3:
    print('use python3 for this script')
    sys.exit()

base = os.environ.get('covid_base')
sys.path.insert(0,base)

pre = 'analysis/'
prog = ['python3']

D = {
      'all_states.py':     ['-c'],
      'all_states.py':     ['-rs', '-N', '5'],
      'one_state.py':      ['HI', '-rs'],
      'one_state.py':      ['SC', '-N', '10'],
      'us_by_counties.py': ['-rs', '-N', '5'],
      
      'trends.py':         ['-n','4', '-N', '10'],
      'country.py':        ['Mexico', '-c', '-N', '7'],
      'country.py':        ['Switzerland'],
      'eu.py':             ['-N', '3'] }
      
errors = []

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