# 1
# Remove individual problematic entries:

popif(D,'Brockton;MA;;US')
popif(D,'LeSeur;MN;;US')
popif(D,'Manchester;NH;;US')
popif(D,'Nashua;NH;;US')

# all 4 counties are also present
popif(D,'Kansas City;MO;;US')

popif(D,'Southeast Utah;UT;;US')
#popif(D,'Southwest;UT;90049;US')
popif(D,'Southwest UT;Utah;;US')
popif(D,'TriCounty;UT;;US')

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
                
for fips, no_fips in rL:
    if no_fips == 'Southwest Utah;UT;;US':
        D[no_fips]['cases'].insert(0,0)
        D[no_fips]['deaths'].insert(0,0)

    # special for France, transfer fips to no_fips
    if no_fips == ';;;France':
        fix_it(fips, no_fips)
        popif(D,fips)
                
    else:
        # transfer no_fips to fips
        try:
            fix_it(no_fips, fips)
        except AssertionError:
            print no_fips, fips
            print D[no_fips]['cases']
            print D[fips]['cases']
            print 
        popif(D,no_fips)
        
