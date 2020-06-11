import sys
import util as ut
import numpy as np
from matplotlib import pyplot as plt


date_info, D = ut.load_db()
kL = ut.key_list_for_search_term('US')

mode = "deaths"

rL = list()
big = list()

for k in kL:
    mL = D[k][mode]
    try:
        n = int(mL[-1])
    except ValueError:
        n = 0
    if n > 49:
        big.append((k,n))
    rL.append(n)
    
for e in sorted(big, key = lambda x: x[1], reverse=True):
    print e[0].split(';')[0].ljust(16), str(e[1]).rjust(5)
            
print '-'.rjust(2), len(rL)

for i in range(4):
    print str(i).rjust(2), rL.count(i)
    
    
    
#rL = [n for n in rL if 3 < n < 49]

rL.sort()
rL = rL[:-100]

data = np.array(rL)
plt.scatter(range(len(data)),data, s=25, color='b')
# plt.hist(data, bins = 45???)

plt.savefig('example.png')
