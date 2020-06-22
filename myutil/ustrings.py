sep = ';'
sep2 = '#'

eu_majors = ['Austria', 'Belgium', 'Czechia', 'Denmark', 'Finland',
             'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
             'Italy', 'Netherlands', 'Poland', 'Portugal', 'Spain',
             'Sweden']


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

state_to_abbrev = dict(zip(states,abbrev))
abbrev_to_state = dict(zip(abbrev,states))

territories_to_abbrev = {
    'Puerto Rico':'PR',
    'Guam':'GU',
    'Northern Marianas Islands':'MP',
    'Virgin Islands':'VI',
    'American Samoa':'AS' }

if __name__ == "__main__":
    D = state_to_abbrev
    for k in sorted(D.keys()):
        print(D[k], k)



    
    