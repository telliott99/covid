import sys
import util as ut

D = ut.clargs()
mode = D['mode']
                 
countries = ut.eu_majors + ['Norway','Switzerland']
#countries = ['France', 'Germany', 'Italy', 'Spain']

countries.sort()

date_info, D = ut.load_db()
rL = []

# some places like France have territories we don't want 
# so we search with ';;;France'
for c in countries:
    sD = D[';;;' + c]
    vL = sD[mode]
    rL.append(vL)
    
s = ut.fmt_csv(countries,rL)
print s
