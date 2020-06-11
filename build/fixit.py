import sys


#from util_path import util as ut
sys.path.insert(0,'/Users/telliott/Dropbox/covid')
import util.db as utdb
import util.strings as uts

sep = uts.sep   # ;
date_info, D = utdb.load_db()

#----------------------------

def popif(D,k):
    try:
        D.pop(k)
    except:
        pass
        
# 1
# Remove individual problematic entries:

popif(D,'Brockton;Massachusetts;;US')
popif(D,'LeSeur;Minnesota;;US')
popif(D,'Manchester;New Hampshire;;US')
popif(D,'Nashua;New Hampshire;;US')

# all 4 counties are also present
popif(D,'Kansas City;Missouri;;US')

popif(D,'Southeast Utah;Utah;;US')
popif(D,'Southwest;Utah;90049;US')
popif(D,'Southwest Utah;Utah;;US')
popif(D,'TriCounty;Utah;;US')

#----------------------------

# 2

'''
fix France!
03-23, assigned to           ;French Polynesia;;France
04-10 to 4-12, assigned to   ;;00250;France
04-10 to 4-12, assigned to   ;;250;France
'''

# we do the latter two below when we update for zip codes
# fix 03-23

cL1 = D[';;;France']['cases']
dL1 = D[';;;France']['deaths']

cL2 = D[';French Polynesia;;France']['cases']
dL2 = D[';French Polynesia;;France']['deaths']

cL1[1] = cL2[1]
dL1[1] = dL2[1]
 
#----------------------------

def fix_it(old,new):
    if not old in D:
        return
    if not new in D:
        D[new] = D[old]
        
    cL = utdb.merge(D[old]['cases'],D[new]['cases'])
    dL = utdb.merge(D[old]['deaths'],D[new]['deaths'])
    mD = {'cases':cL, 'deaths':dL }
    D[new] = mD
    
#----------------------------
# 3:  Utah is bad!
# see: db problems.txt

'''

fix_it('Bear River;Utah;;US','Box Elder;Utah;49003;US')
popif(D,'Bear River;Utah;;US')

fix_it('Weber-Morgan;Utah;;US','Weber;Utah;49057;US')
popif(D,'Weber-Morgan;Utah;;US')

k1 = 'Dukes and Nantucket;Massachusetts;;US'
k2 = 'Dukes;Massachusetts;25007;US'
fix_it(k1,k2)
popif(D,k1)

'''

#----------------------------

def check():
    rL = list()
    for k in D:
        county,state,fips,country = k.split(sep)
        if fips == '':
            continue
        alt = sep.join([county,state,'',country])
        if alt in D:
            rL.append((k,alt))
    return rL


rL = check()

# 4
# 67 places acquired fips at some point after day 1
# print len(rL)
    
custom = [';Virgin Islands;;US',
          ';Puerto Rico;;US',
          ';Northern Mariana Islands;;US']

for fips, no_fips in rL:
    # special for France, transfer fips to no_fips
    if no_fips == ';;;France':
        fix_it(fips, no_fips)
        popif(D,fips)
        
    elif no_fips in custom:
        continue   # fix below
        
    else:
        # transfer no_fips to fips
        fix_it(no_fips, fips)
        popif(D,no_fips)
        
#----------------------------

# 5
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

fix_it(v, v78)
fix_it(v78000, v78)
fix_it(v00078, v78)
for k in [v,v78000,v00078]:
    popif(D,k)

p =      ';Puerto Rico;;US'
p72 =    ';Puerto Rico;72;US'
p00072 = ';Puerto Rico;00072;US'
fix_it(p, p72)
fix_it(p00072, p72)
for k in [p,p00072]:
    popif(D,k)

m =      ';Northern Mariana Islands;;US'
m69 =    ';Northern Mariana Islands;69;US'
m69000 = ';Northern Mariana Islands;69000;US'
fix_it(m, m69)
fix_it(m69000, m69)
for k in [m,m69000]:
    popif(D,k)
    
# 5
# District of Columbia

k1 = 'District of Columbia;District of Columbia;11001;US'
k2 = 'District of Columbia;DC;11001;US'

try:
    fix_it(k1,k2)
except:
    pass
popif(D,k1)

utdb.save_db(D)