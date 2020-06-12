from operator import itemgetter

import udates
import umath

def fmt_dates(conf):
    n = conf['n']
    dates = udates.all_dates[-n:]
    dL = ['/'.join(d.split('-')[1:]) for d in dates]
    return dL

#-----------------------

# for now, make the last day the latest in the db

def fmt_screen(data, labels, conf):    
        
    # rL is data, a list of lists of ints
    # trim the data
    n = conf['n']
    if conf['delta']:
        n += 1
    
    rL = [e[-n:] for e in data]
    
    # option: delta
    if conf['delta']:
        tmp = []
        for sL in rL:
            tmp2 = []
            for i in range (1,len(sL)):
                tmp2.append(sL[i] - sL[i-1])
            tmp.append(tmp2)
        rL = tmp
    
    # options:  totals, stats, sorted
    # defaults: T T F
    
    if conf['totals']:
        labels = labels + ['total']
        rL.append(umath.totals(rL))

    # find the largest data value, use for vpad for data
    vpad = 0
    for vL in rL:
        MX = max([len(str(n)) for n in vL])
        if MX > vpad:
            vpad = MX
            
    # min vpad is 7
    vpad = max(MX,5) + 2
    
    #-------------------
        
    # find the longest label 
    # used only if not trimming, which only happens
    # if stats are used
    pad = max(len(c) for c in labels) + 2
    
    # stats    
    stats = [round(umath.stat(vL),3) for vL in rL]

    # build rows, leave stats separate to allow sort
    pL = []
    for label,vL,st in zip(labels,rL,stats):
        # return early if not using stats
        # so build that version using pad
        values = ''.join([str(n).rjust(vpad) for n in vL])
        
        if conf['stats']:
            tmp = [label,values,st]
        else:
            tmp = ''.join([label.ljust(pad), values])
        pL.append(tmp)
    
    #-------------------
    
    dL = fmt_dates(conf)
    
    dates = ''.join([d.rjust(vpad) for d in dL])
    dateline = ''.rjust(pad) + dates

    if not conf['stats']:
        return dateline + '\n' + '\n'.join(pL)
    
    if conf['sort']:
        totals_line = pL.pop()
        pL.sort(key=itemgetter(2), reverse=True)
        pL.append(totals_line)
 
    # must come after sort, lose totals in the process    
    N = conf['N']
    if N < 51:
        pL = pL[:N]
    
    # so now we pad labels based on what remains
    labels = [t[0] for t in pL]
    pad = max(len(c) for c in labels) + 2
    dateline = ''.rjust(pad) + dates
    
    tL = []
    for label,values,st in pL:
        s = label.ljust(pad)
        s += values
        s += "  %s" % str(round(st,3))
        tL.append(s)
        
    return dateline + '  stats\n' + '\n'.join(tL)

