import sys, os
base = os.environ.get('covid_base')

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path = [base] + sys.path
myutil = base + '/myutil'
if not myutil in sys.path:
    sys.path.insert(0, myutil)

def pprint(conf_dict, msg=None):
    if msg:  print(msg)
    for k in sorted(conf_dict.keys()):
        if conf_dict[k]:
            print(k.ljust(10),conf_dict[k])
    print('\n')

def fmt(labels,pL,conf):
    # format as desired
        
    # format for screen
    if not conf['csv']:
        extra = 1
        m = max([len(e) for e in labels])
        labels = [e.ljust(m + extra) for e in labels]
        
        n = 0
        for vL in pL:
            # don't count the last value if stats
            if conf['rate']:
                for e in vL[:-1]:
                    if len(e) > n:
                        n = len(e)
            else:
                for e in vL:
                    if len(e) > n:
                        n = len(e)
        tmp = []
        for vL in pL:
            vL = [e.rjust(n + extra) for e in vL]
            tmp.append(''.join(vL))
        pL = tmp
        
        tmp = []
        for l,v in zip(labels,pL):
            tmp.append(l + v)
        text = '\n'.join(tmp)
    
    # format csv
    else:
        tmp = []
        for l,vL in zip(labels,pL):
            tmp.append(l + ',' + ','.join(vL))
        text = '\n'.join(tmp)
        
    return text
