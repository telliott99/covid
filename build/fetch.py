# python fetch.py 06-24

import urllib2, sys, os

src = sys.argv[1]
date = sys.argv[2]

fn = date + '.csv'
path = 'csv.source/' + fn
print 'fn:   ' + fn
print 'path: ' + path


if os.path.exists(path):
    print 'file exists'
    if len(sys.argv) > 2:
        print 'override'
    else:
        print 'quiting'
        sys.exit()
        

print 'requesting file'

yr,mo,day = date.split('-')

url = 'https://raw.githubusercontent.com/'
url += 'CSSEGISandData/COVID-19/master/csse_covid_19_data/'
url += 'csse_covid_19_daily_reports/%s-%s-%s.csv' % (mo,day,yr)

# print('url ', url)

def download(url):
    fh = urllib2.urlopen(url)
    return fh.read()
    
data = download(url)

with open(path,'w') as fh:
    fh.write(data)

