import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)

states = [
'Alabama','Alaska','Arizona','Arkansas',
'California', 'Colorado', 'Connecticut',
'Delaware','District of Columbia',
'Florida', 'Georgia', 'Hawaii',
'Idaho', 'Illinois', 'Indiana', 'Iowa',
'Kansas', 'Kentucky', 'Louisiana',
'Maine', 'Maryland', 'Massachusetts', 'Michigan',
'Minnesota', 'Mississippi', 'Missouri', 'Montana',
'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
'New Mexico', 'New York', 'North Carolina', 'North Dakota',
'Ohio', 'Oklahoma', 'Oregon', 
'Pennsylvania', 'Rhode Island', 'South Carolina', 
'South Dakota', 'Tennessee', 'Texas', 'Utah',
'Vermont', 'Virginia', 'Washington',
'West Virginia', 'Wisconsin', 'Wyoming']

abbrev = [
'AL','AK','AZ','AR','CA','CO','CT','DE','DC',
'FL','GA','HI','ID','IL','IN','IA',
'KS','KY','LA','ME','MD','MA','MI',
'MN','MS','MO','MT','NE','NV','NH','NJ',
'NM','NY','NC','ND','OH','OK','OR',
'PA','RI','SC','SD','TN','TX','UT',
'VT','VA','WA','WV','WI','WY']

terr = [
'American Samoa', 'Guam', 'Northern Mariana Islands',
'Puerto Rico','Virgin Islands']

tabbrev = [
'AS','GU','MP','PR','VI']

state_to_abbrev = dict(zip(states, abbrev))
abbrev_to_state = dict(zip(abbrev,states))
terr_to_abbrev = dict(zip(terr,tabbrev))
abbrev_to_terr = dict(zip(tabbrev,terr))
    
data='''
AL	01
AK	02
AZ	04
AR	05
CA	06
CO	08
CT	09
DE	10
DC	11
FL	12
GA	13
HI	15
ID	16
IL	17
IN	18
IA	19
KS	20
KY	21
LA	22
ME	23
MD	24
MA	25
MI	26
MN	27
MS	28
MO	29
MT	30
NE	31
NV	32
NH	33
NJ	34
NM	35
NY	36
NC	37
ND	38
OH	39
OK	40
OR	41
PA	42
RI	44
SC	45
SD	46
TN	47
TX	48
UT	49
VT	50
VA	51
WA	53
WV	54
WI	55
WY	56
AS	60
GU	66
MP	69
PR	72
VI	78
'''

# AS American Samoa
# MP Northern Marianas Islands

def get_abbrev_to_fips():
    L = data.strip().split('\n')
    D = {}
    for e in L:
        st, fips = e.strip().split('\t')
        D[st] = fips
    return D

abbrev_to_fips = get_abbrev_to_fips()
    
def get_fips_to_abbrev():
    D = {}
    for k in abbrev_to_fips:
        v = abbrev_to_fips[k]
        D[v] = k
    return D
    
fips_to_abbrev = get_fips_to_abbrev()

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

if __name__ == "__main__":
    for state in states:
        abbrev = state_to_abbrev[state]
        fips = abbrev_to_fips[abbrev]
        pop = state_to_pop[state]
        print(','.join([state, abbrev, fips, pop]))
        assert fips_to_abbrev[fips] == abbrev
        



    
    