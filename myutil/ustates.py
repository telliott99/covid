import udb
sep = udb.sep

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
'AL','AK','AZ','AR',
'CA','CO','CT',
'DE','DC',
'FL','GA','HI',
'ID','IL','IN','IA',
'KS','KY','LA',
'ME','MD','MA','MI',
'MN','MS','MO','MT',
'NE','NV','NH','NJ',
'NM','NY','NC','ND',
'OH','OK','OR',
'PA','RI','SC',
'SD','TN','TX','UT',
'VT','VA','WA',
'WV','WI','WY']

terr = [
'American Samoa', 
'Guam', 
'Northern Mariana Islands',
'Puerto Rico',
'Virgin Islands']

tabbrev = [
'AS',
'GU',
'MP',
'PR',
'VI']

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

def get_state_to_fips():
    D = {}
    for state in states:
        abbrev = state_to_abbrev[state]
        fips = abbrev_to_fips[abbrev]
        D[state] = fips
    return D
    
state_to_fips = get_state_to_fips()
        
#-----------------------------------

def key_for_state(state):
    fips = state_to_fips[state]
    return sep.join(['',state,fips,'US'])

def key_list_for_states():
    kL = [key_for_state(s) for s in states]
    return kL
    
#-----------------------------------
        
if __name__ == "__main__":

    for state in states:
        fips = state_to_fips[state]
        pop = state_to_pop[state]
        print(','.join([state, abbrev, fips, pop]))
        assert fips_to_abbrev[fips] == abbrev
        



    
    