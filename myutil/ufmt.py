import sys
from operator import itemgetter

import udates
import umath

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

def do_no_data(conf):
    c = conf['arg']
    print('no data for: %s' % c)
    if "Korea" in c:
        print('try: "Korea, South"')
    sys.exit()

def trim_columns(rL, conf):
    if len(rL) == 0:
        do_no_data()
        
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

#-----------------------

# for now, make the last day the latest in the db

def fmt(data, labels, conf, csv=False):
    #pprint(conf)
    rL = trim_columns(data,conf)

    # options:  totals, stats, sorted
    # defaults: T       F      F
    
    if conf['totals']:
        conf['totals'] = umath.totals(rL)

    #-------------------

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
    vpad = max(MX,5) + 2
    conf['vpad'] = vpad
    
    #-------------------
    
    # determine pad for labels column
    pad = max([len(c) for c in labels]) + 2
    pad = max(pad, len('totals') + 2)
    conf['pad'] = pad
    
    #pprint(conf)
        
    #-------------------

    # handle the case if stats are *not* used first
    # return early if not using stats

    if not conf['stats']:
        return final_assembly(labels,rL,conf)
    
    #-------------------
    
    # keep stats as floats until sorted
    stats = [round(umath.stat(vL),3) for vL in rL]

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
