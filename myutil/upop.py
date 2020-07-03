import sys, os, csv
base = os.environ.get('covid_base')
sys.path.insert(0,base)

popD = {}
with open(base + '/pop.db.txt') as fh:
    data = fh.read().strip().split('\n')
    for line in data:
        k,pop = line.strip().split('#')
        popD[k] = pop
