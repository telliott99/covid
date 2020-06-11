import udates
import umath


def fmt_dates(n, last=None):
    dates = udates.all_dates
    
    if not last:
        dates = dates[-n:]
    else:
        j = dates.index(last)
        dates = dates[j-n+1:j+1]
        
    dL = ['/'.join(d.split('-')[1:]) for d in dates]
    return dL

#-----------------------

# rL is data, a list of lists of ints
# for now, make the last day the latest in the db

def fmt_new(data, labels, conf):       
    n = conf['n']
    rL = [e[-n:] for e in data] 
    
    # find the largest value   
    vpad = 0
    for vL in rL:
        MX = max([len(str(n)) for n in vL])
        if MX > vpad:
            vpad = MX    
    vpad = max(MX,5) + 2

    labels = labels + ['total'] 
    # find the longest label  
    pad = max(len(c) for c in labels) + 2

    #-------------------
    
    pL = []
    for label,vL in zip(labels,rL):
        tmp = [label.ljust(pad)]
        tmp.extend([str(n).rjust(vpad) for n in vL])
        pL.append(tmp)
        
    return [''.join(sL) for sL in pL]
    
#-----------------------

# older

def fmt_screen(labels,data,num=10,dates=None):
    a = max(len(c) for c in labels) + 1
    b = 0
    for vL in data:
        MX = max([len(str(n)) for n in vL[-num:]])
        if MX > b:
            b = MX
            
    b = max(MX,5) + 1
    rL = list()
    
    for c,vL in zip(labels,data):
        tmp = [c.ljust(a)]
        tmp.extend([str(n).rjust(b) for n in vL[-num:]])
        rL.append(''.join(tmp))
    result = '\n'.join(rL)
    return a,b,result
    
def fmt_csv(labels,data,num=10):
    rL = list()
    for c,vL in zip(labels,data):
        tmp = [c] + [str(n) for n in vL[-num:]]
        rL.append(','.join(tmp))
    return '\n'.join(rL)

