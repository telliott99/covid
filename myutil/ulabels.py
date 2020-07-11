# labels, dates and totals

import sys, os
base = os.environ.get('covid_base')

if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import udb, udates, umath, ufmt
sep = udb.sep

from ustates import state_to_abbrev as abbD

def get_dates(conf):
    n = conf['n']
    first = conf['first']
    dates = udates.generate_dates(first)
    dates = dates[-n:]
    dL = ['/'.join(d.split('-')[1:]) for d in dates]
    return dL

# kL is a real key list
# we need to deduce appropriate labels

def generate_labels(kL, conf):
    labels = []
    for k in kL:
        county,state,fips,country = k.strip().split(sep)
        if county != '':
            if 'counties' in conf['names']:
                st = abbD[state]
                labels.append(county + ' ' + st)
            else:
                labels.append(county)
                
        elif state != '':
            labels.append(state)
        else:
            labels.append(country)
    return labels

# in this new design, we generate csv always
def assemble(kL, rL, conf):

    #ufmt.pprint(conf)
    #sys.exit()

    # labels are in the first column
    labels = generate_labels(kL, conf)
    
    # these are the rows, values converted to str
    pL = []
    for vL in rL:    
        pL.append([str(n) for n in vL])
        
    # next add dates as the first row     
    dL = get_dates(conf)
    if conf['rate']:
        dL.append('stat')
    pL = [dL] + pL
   
    # add a space to the first col, first row
    labels = [''] + labels
        
    if conf['total']:
        # add a space to the first col, last row
        labels.append('total')
    
        # conf['totals'] contains the actual values
        tL = conf['totals_line']
        if conf['rate']:
            tL.append(round(umath.stat(tL), 3))   
            
        # convert the last row to str as well                     
        last = [str(v) for v in tL]
        pL += [last]
    
    # add an extra 2 spaces to each value in the last column
    if conf['rate']:
        for vL in pL:
            vL[-1] = '  ' + vL[-1]
        
    return labels, pL

