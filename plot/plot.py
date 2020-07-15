# p3 plot.py -n 120 -c 10 -o -p --csv --no_dates

import sys, os, subprocess

import scipy.signal as signal

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
util = base + '/myutil'
if not util in sys.path:
    sys.path.insert(0, util)

import ufmt
from analyze import *

#ufmt.pprint(conf)

names = ['US', 'France']
rL = []

for name in names:
    conf['names'] = [name]
    text = get_results(conf)
    vL = text.split(',')[1:]  # leading ','
    rL.append([int(s) for s in vL])


vL = rL[0]

# smooth
#f = signal.savgol_filter
#vL = f(vL,21,3)
    
#---------------------------------------

import plotly.graph_objects as go

plt_us = go.Scatter(
    x=list(range(len(vL))),
    y=vL,
    line={'color':'blue', 'width':3})
    
fig = go.Figure(plt_us)

#---------------------------------------

vL = rL[1]

# smooth
#vL = f(vL,21,3)

plt_eu = go.Scatter(
    x=list(range(len(vL))),
    y=vL,
    line={'color':'red', 'width':3})

fig.add_trace(plt_eu)

fig.update_layout(yaxis=dict(range=[0,250]))

fig.show()

