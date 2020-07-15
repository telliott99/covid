# all data trimming, sorting and stats done here
# the values returned are ready to format for printing
# or to feed to a plot or map script

import sys, os

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
util = base + '/myutil'
if not util in sys.path:
    sys.path.insert(0, util)

import umath
import upop
import udb

popD = upop.popD
sep = udb.sep
 
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

# mutating, drops keys for any not in popD:  Unassigned et al.
def do_pop_normalization(kL, rL):

    tmp1 = []
    tmp2 = []
    for k, vL in zip(kL,rL):
        if not k in popD:
        
        # it is OK to just skip it
        # we get labels from keys these days, later
            if k.split(sep)[0] not in ['Unassigned', 'unassigned']:    
                print('KeyError, key not in pop_dict:')
                print(k)
            continue
        
        tmp1.append(k)
        tmp2.append(vL)
    
    kL = tmp1
    rL = tmp2

    #------

    #print('do_pop_normalization')
    ret = []
    popL = []
        
    # obtain the population for each key
    for k in kL:
        v = popD[k]
        popL.append(v)

    for pop,vL in zip(popL,rL):
    
        # save the normalized values
        ret.append(normalize(pop,vL))
      
    #print(kL)  
    #print(ret)
    
    total_pop = sum([int(s) for s in popL])
    
    return kL, ret, total_pop

#-----------------------

def compute_average(rL, conf):
    def mean(sL):
        result = int(sum(sL)*1.0/len(sL))
        return result

    n = conf['average']    
    ret = []
    
    # trim early to avoid unnecessary computations
    if conf['N']:
        N = conf['N']
        rL = rL[:N]
    
    for vL in rL:
        tmp = []
        for i in range(n, len(vL)):
            val = mean(vL[i-n+1:i+1])
            tmp.append(val)
        ret.append(tmp)
    return ret

#-----------------------

def trim_columns(rL, conf):
    if len(rL) == 0:
        do_no_data(conf)
    
    # here is where slice up to u days ago
    if conf['u']:
        u = conf['u']
        rL = [vL[:-u] for vL in rL]
        
    # rL is data, a list of lists of ints
    # trim the data
    # affected by option delta
    n = conf['n']
    if conf['delta']:
        n += conf['delta']
        
    if conf['average']:
        n += conf['average'] - 1
        
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
    
    conf['totals_line'] = umath.totals(rL)
    
    # if normalizing
    # also adjust totals to total population
    
    if conf['pop']:
        kL, nL, total_pop = do_pop_normalization(kL,rL)
        
        tL = conf['totals_line']
        conf['totals_line'] = normalize(total_pop, tL)
        
        rL = nL
        
    if conf['average']:
        rL = compute_average(rL, conf)

    pL = []
    
    # special case b/c eu key not in keylist
    
    if 'eu' in conf['names']:
        if kL[0] == ';;;Austria':
            if conf['only']:
                tL = [str(n) for n in conf['totals_line']]
                return [';;;eu'], [conf['totals_line']]

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
    # totals are calculated but not yet attached
    
    if conf['N']:
        N = conf['N']
        rL = rL[:N]
        kL = kL[:N]

    return kL, rL
            