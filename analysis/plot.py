import sys, os, subprocess

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.udates as udates
import myutil.ufile as ufile
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath

#---------------------------------------

conf = uinit.clargs()
mode = conf['mode']

if not conf['arg']:
    print('please supply the name of a country')
    sys.exit()
    
country = conf['arg']

sep = ustrings.sep      # ;
path_to_db = base + '/db.max.txt'

date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#---------------------------------------

kL = ukeys.key_list_for_search_term(country, mode="country")

rL = []
for k in kL:
    try:
        rL.append(D[k][conf['mode']])
    except:
        print('error with: %s' % k)
        
vL = umath.totals(rL)
pL = []

for x,y in zip(vL[:-1],vL[1:]):
    pL.append(y - x)
#print(pL)

'''
sL = []
n = 10
for i in range(n,len(pL)-n):
    sL.append(sum(pL[i-n:i+n+1])/(1.0*(n+1)))
'''

import plotly.graph_objects as go

plt = go.Scatter(
    x=list(range(len(pL))),
    y=pL,
    line={'color':'blue', 'width':3})

fig = go.Figure(plt)

fig.update_layout(yaxis=dict(range=[0,50000]))

fig.show()


