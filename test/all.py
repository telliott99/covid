import sys, os
import subprocess

if sys.version_info[0] < 3:
    print('use python3 for this script')
    sys.exit()

base = os.environ.get('covid_base')
sys.path.insert(0,base)

prog = ['python3']

errors = []

script = 'analyze.py'
path = base + '/' + script
cmds = prog + [path, 'SC', '-q']

for arg in 'acoprsw':
    print('running: python3 ' + script + 'SC -q' + ' -' + arg)
    r = subprocess.run(cmds + ['-' + arg])
    if (r.returncode != 0):
        errors.append(script)

options = [   
['US', '-op'],
['US', '-p', '-N', '5'],
['US', '-t', '-N', '5'],
['US', '-c', '10', '-N', '5'],
['US', '-rs', '-N', '5'],
['HI', '-rs'],
['SC', '-N', '3'],
['Mexico', '-c', '-N', '3'],
['Switzerland'],
['Germany', '-N', '3', '-o'],
['Russia', '-po', '-q'],
['counties', '-s', '-c', '10', '-N', '30'] ]

      
for args in options:
    cmds = prog + [script] + args
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