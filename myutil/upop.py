import sys, os
base = os.environ.get('covid_base')

s = '''
;;;Australia#24.99
;;;Austria#8.859
;;;Belgium#11.46
;;;Canada#37.59
;;;Czechia#10.69
;;;Denmark#5.806
;;;Estonia#1.329
;;;Finland#5.518
;;;France#66.99
;;;Germany#83.02
;;;Greece#10.72
;;;Hungary#9.773
;;;Ireland#4.904
;;;Italy#60.36
;;;Latvia#1.92
;;;Lithuania#2.794
;;;Netherlands#17.28
;;;Poland#30.97
;;;Portugal#10.28
;;;Spain#46.94
;;;Sweden#10.23
'''


popD = {}
with open(base + '/pop.db.txt') as fh:
    data = fh.read().strip().split('\n')
    for line in data:
        k,pop = line.strip().split('#')
        popD[k] = pop

for line in s.strip().split('\n'):
    k,pop = line.strip().split('#')
    k = k[3:]
    popD[k] = int(float(pop)*1e6)

