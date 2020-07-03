# python extract_pop.py > pop.txt

import sys, csv

with open('data/co-est2019-annres.csv') as fh:
    data = fh.read().strip().split('\n')

# remove United States summary
reader = csv.reader(data[1:])
for e in reader:
    if e[0].startswith('.'):
        e[0] = e[0][1:]
    county, state = e[0].split(',')
    state = state.strip()
    
    county = county.strip()
    # Parish in LA, Borough in Alaska, 
    # County elsewhere
    # except Aleutians West Census Area
    
    for sfx in ['County', 'city', 'City and Borough', 
                'Borough', 'Parish', 'Census Area',
                'Municipality']:
        if county.endswith(sfx):
            county = county.replace(sfx,'').strip()
    
    loc = ';'.join([county,state])
    
    pop = e[-1].replace(',','')
    pL = [loc,pop]
    print ','.join(pL)

with open('extra.txt') as fh:
    data = fh.read().strip().split('\n')
    data = [e for e in data if not e == '']

for e in data:
   print e 