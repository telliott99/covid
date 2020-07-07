import sys, os, subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/test')

subprocess.run(['python3', 'test/test_scripts.py'])
subprocess.run(['python3', 'test/test_maps.py'])