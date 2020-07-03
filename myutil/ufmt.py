import sys
from operator import itemgetter

import udates
import umath

from ustates import state_to_abbrev as abbD
from ustrings import sep as sep

def pprint(conf):
    for k in sorted(conf.keys()):
        print(k.ljust(10),conf[k])
    print('\n')

def get_dates(conf):
    n = conf['n']
    first = conf['first']
    
    dates = udates.generate_dates(first)
    dates = dates[-n:]
    dL = ['/'.join(d.split('-')[1:]) for d in dates]
    #print('dL', dL)
    return dL
    
def do_vpad(rL,conf):
    # longest data value determines vpad for data
    
    vpad = 0
    for vL in rL:
        MX = max([len(str(n)) for n in vL])
        if MX > vpad:
            vpad = MX
            
    if conf['totals']:
        vL = conf['totals']
        MX = max([len(str(n)) for n in vL])
        if MX > vpad:
            vpad = MX
            
    # min vpad
    m = 1
    vpad = max(MX,5) + m
    conf['vpad'] = vpad
    # altered conf holds the value

def do_labels_pad(labels, conf):
    m = 2
    pad = max([len(c) for c in labels]) + m
    pad = max(pad, len('totals') + m)
    conf['pad'] = pad

def do_no_data(conf):
    c = conf['arg']
    print('no data for: %s' % c)
    if "Korea" in c:
        print('try: "Korea, South"')
    sys.exit()

def trim_columns(rL, conf):
    if len(rL) == 0:
        do_no_data(conf)
        
    # rL is data, a list of lists of ints
    # trim the data
    n = conf['n']
    if conf['delta']:
        n += 1    
    rL = [e[-n:] for e in rL]
    
    # option: delta
    if conf['delta']:
        tmp = []
        for sL in rL:
            tmp2 = []
            for i in range (1,len(sL)):
                tmp2.append(sL[i] - sL[i-1])
            tmp.append(tmp2)
        rL = tmp
    return rL
    
def final_assembly(labels,rL,conf):
    # print('do_no_stats')
    #pprint(conf)

    if conf['N']:
        N = conf['N']
        rL = rL[:N] + ['']
        labels = labels[:N] + ['...']
        
    vpad = conf['vpad']
    
    # pad may have shortened with fewer labels
    do_labels_pad(labels,conf)
    pad = conf['pad']

    dL = get_dates(conf)
    dates = ''.join([d.rjust(vpad) for d in dL])
    pL = [''.rjust(pad) + dates]
    
    if conf['totals']:
        labels.append('total')
        tL = conf['totals']
        if conf['stats']:
            tL.append(str(round(umath.stat(tL),3)))
        rL.append(tL)
    
    for label,vL in zip(labels,rL):
        values = ''.join([str(n).rjust(vpad) for n in vL])
        pL.append(label.ljust(pad) + values)
        
    return '\n'.join(pL)

def do_pop_normalization(kL, rL):
    from upop import popD
    
    #print('do_pop_normalization')
    ret = []
    popL = [popD[k] for k in kL]
    
    for pop,vL in zip(popL,rL):
        pop = float(pop)/100000.0
        vL = [v/pop for v in vL]
        vL = [int(f) for f in vL]
        ret.append(vL)
    return ret

#=======================

# for now, make the last day the latest in the db

def fmt(data, kL, conf, csv=False):

    # switched to passing in a real kL for most cases
    # so, must generate labels here:

    if conf['regions'] == 'eu':  
    # kL is not really just a list of countries
        labels = kL
    
    else:
        labels = []    
        for k in kL:
            county,state,fips,country = k.strip().split(sep)
            r = conf['regions']
            
            if r == 'states':
                labels.append(state)
                
            elif r == 'one_country':
                if state == '':
                    labels.append(country)
                else:
                    labels.append(state)
                    
            elif r == 'group of countries':
                labels.append('not done')
                
            elif r == 'counties':
                if conf['show_state']:
                    abbrev = abbD[state]
                    labels.append(county + ', ' + abbrev)
                else:
                    labels.append(county)
    
    # new idea:
    # compute stats on the last 14 days
    # regardless of what we display
    
    # keep stats as floats until sorted
    
    rL = data
                    
    #pprint(conf)
    rL = trim_columns(rL,conf)
    
    # no totals if normalizing

    if conf['pop']:
        rL = do_pop_normalization(kL,rL)
        conf['totals'] = False

    # options:  totals, stats, sorted
    # defaults: T       F      F
    
    #pprint(conf)
    
    if conf['totals']:
        conf['totals'] = umath.totals(rL)

    #-------------------

    # determine pad for values
    do_vpad(rL, conf)
    vpad = conf['vpad']
    
    # determine pad for labels column
    
    do_labels_pad(labels,conf)
    pad = conf['pad']
    
    #pprint(conf)
        
    #-------------------

    # handle the case if stats are *not* used first
    # return early if not using stats

    if not conf['stats']:
        return final_assembly(labels,rL,conf)
    
    #-------------------
    stats = [round(umath.stat(vL[-14:]),3) for vL in rL]

    pL = []
    for label,vL,st in zip(labels,rL,stats):
        pL.append([label,vL,st])
        
    if conf['sort']:
        pL.sort(key=itemgetter(2), reverse=True)
    
    labels = []
    rL = []
    for label,vL,st in pL:
        labels.append(label)
        rL.append(vL + [str(st).ljust(5)])
    
    return final_assembly(labels,rL,conf)
