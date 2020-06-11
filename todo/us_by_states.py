import sys
import util as ut

state = sys.argv[1]

mode = "cases"
if len(sys.argv) > 2:
    mode = "deaths"
    
trending = False

date_info, D = ut.load_db()
f = ut.try_int

kL = ut.key_list_for_us_counties()
kL.sort(cmp=ut.custom_sort)

labels = []
for k in kL:
    c,s,fips,y = k.strip().split(ut.sep)
    labels.append(c)

rL = [D[k][mode][-9:] for k in kL]

if trending:
    for sL in rL:
       x = f(sL[-2]) - f(sL[0])
       y = f(sL[-1]) - f(sL[1])
       sL.extend(['  ', str(x),str(y)])

print s
print(ut.fmt_screen(labels, rL))
print