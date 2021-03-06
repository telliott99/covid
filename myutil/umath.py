from scipy import stats as st
from operator import itemgetter

def try_int(n):
    try:
        return int(n)
    except:
        return n

#=================

# merge is used in check.py

def merge(xL,yL):
    assert len(xL) == len(yL)
    rL = list()
    for x,y in zip(xL,yL):
        rL.append(x + y)
    return rL

# total lists of lists

def totals(L):
    tL = list(zip(*L))
    '''
    retL = list()
    for t in tL:
        tmp = 0
        for n in t:
            tmp += n
        retL.append(tmp)    
    '''

    retL = [sum(sL) for sL in tL]
    return retL

def stat(vL, n=10):
    if vL[-1] < n:
        return 0

    try:
        #return sum(vL[-3:])*1.0/sum(vL[:3])
        xL = range(len(vL))
        results = st.linregress(xL,vL)
        slope = results[0]
        m = 1.0*sum(vL)/len(vL)
        return slope*1.0/m
        
    except:
        return None

# return list of diffs for adjacent values
def do_delta(sL,j):
    ret = []
    for i in range (j,len(sL)):
        ret.append(sL[i] - sL[i-j])
    return ret

def quintiles(n):
    if n > 0.08:  return 0.08
    if n > 0.06:  return 0.06
    if n > 0.04:  return 0.04
    if n > 0.02:  return 0.02
    return 0.01
