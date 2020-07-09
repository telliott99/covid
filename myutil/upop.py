import sys, os
base = os.environ.get('covid_base')

data2='''
California,39512223
Texas,28995881
Florida,21477737
New York,19453561
Pennsylvania,12801989
Illinois,12671821
Ohio,11689100
Georgia,10617423
North Carolina,10488084
Michigan,9986857

New Jersey,8882190
Virginia,8535519
Washington,7614893
Arizona,7278717
Massachusetts,6829503
Tennessee,6829174
Indiana,6732219
Missouri,6137428
Maryland,6045680
Wisconsin,5822434

Colorado,5758736
Minnesota,5639632
South Carolina,5148714
Alabama,4903185
Louisiana,4648794
Kentucky,4467673
Oregon,4217737
Oklahoma,3956971
Connecticut,3565287
Utah,3205958

Iowa,3155070
Nevada,3080156
Arkansas,3017804
Mississippi,2976149
Kansas,2913314
New Mexico,2096829
Nebraska,1934408
West Virginia,1792147
Idaho,1787065
Hawaii,1415872

New Hampshire,1359711
Maine,1344212
Montana,1068778
Rhode Island,1059361
Delaware,973764
South Dakota,884659
North Dakota,762062
Alaska,731545
District of Columbia,705749
Vermont,623989
Wyoming,578759

Puerto Rico,3193694
Guam,165718
Virgin Islands,104914
American Samoa,55641
Northern Mariana Islands,55194
'''

def get_state_to_pop():
    L = data2.strip().split('\n')
    D = {}
    for e in L:
        if e == '':
            continue
        st, pop = e.strip().split(',')
        D[st] = pop
    return D
    
state_to_pop = get_state_to_pop()

# Millions

s = '''
;;;Australia#24.99
;;;Austria#8.859
;;;Belgium#11.46
;;;Canada#37.59
;;;China#1393
;;;Czechia#10.69
;;;Denmark#5.806
;;;Estonia#1.329
;;;Finland#5.518
;;;France#66.99
;;;Germany#83.02
;;;Greece#10.72
;;;Hungary#9.773
;;;Ireland#4.904
;;;Italy#60.36
;;;Latvia#1.92
;;;Lithuania#2.794
;;;Netherlands#17.28
;;;Poland#30.97
;;;Portugal#10.28
;;;Russia#144.5
;;;Spain#46.94
;;;Sweden#10.23
;;;US#328.2
'''


popD = {}
with open(base + '/pop.db.txt') as fh:
    data = fh.read().strip().split('\n')
    for line in data:
        k,pop = line.strip().split('#')
        popD[k] = pop

for line in s.strip().split('\n'):
    k,pop = line.strip().split('#')
    popD[k] = int(float(pop)*1e6)

