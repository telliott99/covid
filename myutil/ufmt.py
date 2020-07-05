import sys
from operator import itemgetter

import udates
import umath

from ustates import state_to_abbrev as abbD
from ustrings import sep as sep
from upop import popD

def pprint(conf_dict, msg):
    if conf_dict['verbose'] is False:
        return
    print(msg)
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

def get_dates(conf):
    n = conf['n']
    first = conf['first']
    
    dates = udates.generate_dates(first)
    dates = dates[-n:]
    dL = ['/'.join(d.split('-')[1:]) for d in dates]
    #print('dL', dL)
    return dL
    
def do_labels(kL, conf):
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
    return labels

#-----------------------

def normalize(pop, vL):
    pop = float(pop)/100000.0
    vL = [int(value/pop) for value in vL]
    return vL

def do_pop_normalization(kL, rL):   
    #print('do_pop_normalization')
    ret = []
    popL = [popD[k] for k in kL]
    for pop,vL in zip(popL,rL):
        ret.append(normalize(pop,vL))   
          
    return ret, sum([int(s) for s in popL])

#-----------------------

def do_vpad(rL,conf):
    # longest data value determines vpad for data
    
    vpad = 0
    for vL in rL:
        MX = max([len(str(n)) for n in vL])
        if MX > vpad:
            vpad = MX
            
    if conf['totals']:
        vL = conf['totals_values']
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
    
#-----------------------

def final_assembly(labels,rL,conf):
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
    
    # conf['totals'] contains the actual values
    if conf['totals']:
        labels.append('total')
        tL = conf['totals_values']
        if conf['stats']:
            tL.append('   ' + str(round(umath.stat(tL), 3)))
        rL.append(tL)
    
    for label,vL in zip(labels,rL):
        values = ''.join([str(n).rjust(vpad) for n in vL])
        pL.append(label.ljust(pad) + values)
        
    return '\n'.join(pL)

#=======================

# for now, make the last day 
# the latest entry in the db

def fmt(data, kL, conf, csv=False):
    pprint(conf, 'fmt')

    labels = do_labels(kL, conf)    
    rL = data
                    
    #pprint(conf)
    
    # here is where we trim 
    rL = trim_columns(rL,conf)
    
    conf['totals_values'] = umath.totals(rL)
    
    # normalize totals to total population
    if conf['pop']:
        rL, total_pop = do_pop_normalization(kL,rL)
        tL = conf['totals_values']
        conf['totals_values'] = normalize(total_pop, tL)

    # options:  totals, stats, sorted
    # defaults: T       F      F
    
    #-------------------

    # determine pad for values
    do_vpad(rL, conf)
    vpad = conf['vpad']
    
    # determine pad for labels column
    do_labels_pad(labels,conf)
    pad = conf['pad']
    
    #-------------------

    # handle the case where stats are *not* used
    # return early

    #print(labels[0], rL[0])

    if not conf['stats']:
    
        if conf['sort']:
            pL = []        
            for label,vL in zip(labels,rL):
                pL.append([label,vL])            
            pL.sort(key=itemgetter(-1), reverse=True)
            labels = [t[0] for t in pL]
            rL = [t[1] for t in pL]    
        
        #print(labels[0], rL[0])
        return final_assembly(labels,rL,conf)
    
    #-------------------
    
    # compute stats based on the last 7 days
    i = 7
    
    # unless we trimmed above to fewer than 7 values
    
    # three cases
    
    pL = []

    
    # sort and stats
    if conf['stats']:
        # keep each stat as float until after sort
        stats = [round(umath.stat(vL[-i:]),3) for vL in rL]

        for label, vL, st in zip(labels,rL,stats):
            pL.append([label, vL, st])
            
        if conf['sort']:
            pL.sort(key=lambda t: t[2], 
                    reverse=True)
                    
        labels = []
        rL = []
        for t in pL:
            labels.append(t[0])
            t[1] += [str(t[2]).ljust(5)]
            rL.append(t[1])
            
        #print(labels[0], rL[0])
        return final_assembly(labels,rL,conf)
            