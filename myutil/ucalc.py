# all data trimming, sorting and stats done here
# the values returned are ready to format for printing
# or to feed to a plot or map script


import sys, os
base = os.environ.get('covid_base')

if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

from operator import itemgetter

import umath
from ustates import state_to_abbrev as abbD
from ustrings import sep as sep
from upop import popD

def pprint(conf_dict, msg=None):
    if msg:  print(msg)
    for k in sorted(conf_dict.keys()):
        print(k.ljust(10),conf_dict[k])
    print('\n')
    
def do_no_data(conf):
    c = conf['arg']
    print('no data for: %s' % c)
    if "Korea" in c:
        print('try: "Korea, South"')
    sys.exit()

#-----------------------

def normalize(pop, vL):
    pop = float(pop)/100000.0
    vL = [int(value/pop) for value in vL]
    return vL

def do_pop_normalization(kL, rL):   
    #print('do_pop_normalization')
    ret = []
    try:
        popL = [popD[k] for k in kL]
    except:
        print(k)
        print('pop normalization not yet implemented for this script')
        uinit.bail()
    for pop,vL in zip(popL,rL):
        ret.append(normalize(pop,vL))   
          
    return ret, sum([int(s) for s in popL])

#-----------------------

def trim_columns(rL, conf):
    if len(rL) == 0:
        do_no_data(conf)
        
    # rL is data, a list of lists of ints
    # trim the data
    # affected by option delta
    n = conf['n']
    if conf['delta']:
        n += conf['delta']
    rL = [e[-n:] for e in rL]
    
    if conf['delta']:
        j = conf['delta']
        tmp = []
        for sL in rL:
            tmp.append(umath.do_delta(sL,j))
        rL = tmp
        
    return rL
    
#=======================

# for now, make the last day 
# the latest entry in the db

def calc(kL, rL, conf):
    if conf['verbose']:
        pprint(conf, 'fmt')

    # here is where we trim according to -n
    rL = trim_columns(rL,conf)
    
    conf['totals_values'] = umath.totals(rL)
    
    # if normalizing
    # also adjust totals to total population
    
    if conf['pop']:
        rL, total_pop = do_pop_normalization(kL,rL)
        
        tL = conf['totals_values']
        conf['totals_values'] = normalize(total_pop, tL)

    
    pL = []

    # compute stats based on the last 7 days
    # unless we trimmed above to fewer than 7 values
    i = 7

    # sort only
    if not conf['rate']:
    
        if conf['sort']:
            pL = []        
            for kL, vL in zip(kL,rL):
                pL.append([kL,vL])
            
            # sort on the latest value        
            pL.sort(key=lambda t: t[1][-1], 
                    reverse=True)
                    
            kL = [t[0] for t in pL]
            rL = [t[1] for t in pL]       
    
    # stats (rate) +/- sort
    elif conf['rate']:
        
        # keep each stat as float until after sort
        stats = [round(umath.stat(vL[-i:]),3) for vL in rL]

        for kL, vL, st in zip(kL,rL,stats):
            pL.append([kL, vL, st])
            
        if conf['sort']:
            # sort on the statistic
            pL.sort(key=lambda t: t[2], 
                    reverse=True)
                    
        kL = []
        rL = []
        for t in pL:
            kL.append(t[0])
            t[1] += [str(t[2]).ljust(5)]
            rL.append(t[1])

    # trim the rows at this time
    # totals are not yet attached
    
    if conf['N']:
        N = conf['N']
        rL = rL[:N]
        kL = kL[:N]

    return kL, rL
            