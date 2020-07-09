# these fixes only apply to early days
import sys, os
MX = '--max' in sys.argv

base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1, base + '/myutil')

import udb, udates, ufile, ukeys

from udb import sep

if MX:
    path_to_db = base + '/' + 'db.max.txt'
else:
    path_to_db = base + '/' + 'db.txt'

date_info, D = udb.load_db(path_to_db)
first,last = date_info.split('\n')

#------------------------------------

# four US territories got fips added more than once!

'''
The correct codes are two digits

;Northern Mariana Islands;69;US ;Northern Mariana Islands;;US
;Northern Mariana Islands;69000;US ;Northern Mariana Islands;;US

;Puerto Rico;72;US ;Puerto Rico;;US
;Puerto Rico;00072;US ;Puerto Rico;;US

;Virgin Islands;78;US ;Virgin Islands;;US
;Virgin Islands;78000;US ;Virgin Islands;;US
;Virgin Islands;00078;US ;Virgin Islands;;US
'''

v =      ';Virgin Islands;;US'
v78 =    ';Virgin Islands;78;US'
v78000 = ';Virgin Islands;78000;US'
v00078 = ';Virgin Islands;00078;US'

ukeys.merge_keys(D, v, v78)
ukeys.merge_keys(D, v78000, v78)
ukeys.merge_keys(D, v00078, v78)
for k in [v,v78000,v00078]:
    ukeys.popif(D,k)

p =      ';Puerto Rico;;US'
p72 =    ';Puerto Rico;72;US'
p00072 = ';Puerto Rico;00072;US'

ukeys.merge_keys(D, p, p72)
ukeys.merge_keys(D, p00072, p72)
for k in [p,p00072]:
    ukeys.popif(D,k)

m =      ';Northern Mariana Islands;;US'
m69 =    ';Northern Mariana Islands;69;US'
m69000 = ';Northern Mariana Islands;69000;US'

ukeys.merge_keys(D, m, m69)
ukeys.merge_keys(D, m69000, m69)
for k in [m,m69000]:
    ukeys.popif(D,k)

g66 =      ';Guam;66;US'
g66000 =   ';Guam;66000;US'
g00066 =   ';Guam;00066;US'

ukeys.merge_keys(D, g66000, g66)
ukeys.merge_keys(D, g00066, g66)
for k in [g66000,g00066]:
    ukeys.popif(D,k)

a60 =      ';American Samoa;60;US'
a60000 =   ';American Samoa;60000;US'

ukeys.merge_keys(D, a60000, a60)
ukeys.popif(D,a60000)

#------------------------------------

'''
fix France!
03-23, assigned to           ;French Polynesia;;France
04-10 to 4-12, assigned to   ;;00250;France
04-10 to 4-12, assigned to   ;;250;France
'''

# first one

cL1 = D[';;;France']['cases']
dL1 = D[';;;France']['deaths']

cL2 = D[';French Polynesia;;France']['cases']
dL2 = D[';French Polynesia;;France']['deaths']

cL1[1] = cL2[1]
dL1[1] = dL2[1]

# other two

f250 =    ';;250;France'
f00250 = ';;00250;France'
f =      ';;;France'

ukeys.merge_keys(D, f250, f)
ukeys.merge_keys(D, f00250, f)
for k in [f250, f00250]:
    ukeys.popif(D,k)

#------------------------------------
# US Counties that acquired a FIPS 
# at some point after day 1

kL = [k for k in D if k.endswith(';US')]
kL = [k for k in kL if not ';;' in k]

print('\nmerging with no-fips-key')
for k in kL:
    short = ';'.join(k.split(';')[:2])
    alt = short + ';;US'
    if alt in D:
        ukeys.merge_keys(D, alt, k)
        ukeys.popif(D, alt)
        print(k)

#------------------------------------

def filter(k):
    if k.startswith('Unassigned'):
        return False
    if k.startswith('unassigned'):
        return False
    if k.startswith('Out of'):
        return False
    if 'Unknown' in k or 'Recovered' in k:
        return False
    if 'Princess' in k or 'Out-of' in k:
        return False
    if 'MDOC' in k or 'FCI' in k:
        return False
    if 'Walla Walla County' in k:
        return False
    if 'LeSeur;Minnesota' in k:
        return False
    return True

todo = []
for k in D:
    if not filter(k):
        todo.append(k)
for k in todo:        
    ukeys.popif(D, k)

udb.save_db(D, path_to_db, first, last)

