import sys, os
base = os.environ.get('covid_base')

if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import udb, udates, umath
sep = udb.sep

from ustates import state_to_abbrev as abbD

def pprint(conf_dict, msg=None):
    if msg:  print(msg)
    for k in sorted(conf_dict.keys()):
        if conf_dict[k]:
            print(k.ljust(10),conf_dict[k])
    print('\n')

def get_dates(conf):
    n = conf['n']
    first = conf['first']
    
    dates = udates.generate_dates(first)
    dates = dates[-n:]
    dL = ['/'.join(d.split('-')[1:]) for d in dates]
    #print('dL', dL)
    return dL

def do_labels_pad(labels, conf):
    m = 2
    pad = max([len(c) for c in labels]) + m
    pad = max(pad, len('totals') + m)
    conf['pad'] = pad
    return pad

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
    return vpad

# kL is *usually* a real key list
def process_labels(kL, conf):
    #pprint(conf)
    
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

def assemble(kL, rL, conf, is_key_list=True):

    if is_key_list:
        labels = process_labels(kL, conf)
    else:
        labels = kL
            
    vpad = do_vpad(rL, conf)
    
    # pad may have shortened with fewer labels
    pad = do_labels_pad(labels,conf)

    dL = get_dates(conf)
    
    dates = ''.join([d.rjust(vpad) for d in dL])
    pL = [''.rjust(pad) + dates]
    
    # conf['totals'] contains the actual values
    if conf['totals']:
        labels.append('total')
        tL = conf['totals_values']
        if conf['rate']:
            tL.append('   ' + str(round(umath.stat(tL), 3)))
        rL.append(tL)
    
    for label,vL in zip(labels,rL):
        values = ''.join([str(n).rjust(vpad) for n in vL])
        pL.append(label.ljust(pad) + values)
        
    return '\n'.join(pL)

