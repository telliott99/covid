import sys, os, subprocess
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutils')

conf = uinit.clargs()
ufmt.pprint(conf)