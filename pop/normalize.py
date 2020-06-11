import sys
import util as ut
import population as pop

mode = "cases"
if len(sys.argv) > 1:
    mode = "deaths"

date_info, D = ut.load_db()
mD = pop.run(D)

rL = list()
kL = ut.key_list_for_us_counties()
for k in kL:
    n = mD[k][mode][-1]
    if n == '-':
        n = 0
    else:
        n = int(n)
    
    if n < 5:
        continue
        
    pop = float(mD[k]['pop'])
    fpop = pop/100000
        
    freq = round(n/fpop,1)
    rL.append((k,n,pop,freq))

def f(e):
    return e[3]

rL.sort(key = f, reverse = True)

for i,e in enumerate(rL):
    loc = e[0].split(ut.sep)[:2]
    print str(i+1).rjust(4),
    print ', '.join(loc).ljust(33),
    print str(e[1]).rjust(12),
    print str(e[2]).rjust(12),
    print str(e[3]).rjust(7)

