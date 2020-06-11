This is a project to download and play with the data collated by the [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) folks.

My version of the database is constructed from their database files by **update.py**.  This checks the 'csv.source' directory and if it's not up-to-date, downloads the appropriate data files from their [data](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data).

It's all Python2 code, mainly because I can't be bothered to type 'print(s)' instead of 'print s'.

My database looks like

```
2020-03-22
2020-04-28

Autauga;Alabama;01001;US
0,0,1,4 ...
0,0,0,0 ...

...
``` 


I got an urge to make some analysis normalizing to population.  It took some effort to find the data and fix differences with the entries in the Covid-19 database.

