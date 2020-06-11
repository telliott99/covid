# python fetch_data.py 04-01

import urllib2, sys, os
date = sys.argv[1]

fn = '2020-' + date + '.csv'
path = 'csv.source/' + fn
print 'fn:  ' + fn

if os.path.exists(path):
    print 'file exists'
    if len(sys.argv) > 2:
        print 'override'
    else:
        print 'quiting'
        sys.exit()

print 'file requested'

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/%s-2020.csv' % date

def download(url):
    fh = urllib2.urlopen(url)
    return fh.read()
    
data = download(url)

with open(path,'w') as fh:
    fh.write(data)

