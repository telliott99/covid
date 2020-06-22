This is a project to download and play with the data collated by the [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) folks.

My version of the database is constructed from their database files by **update.py**.  This checks the 'csv.source' directory and if it's not up-to-date, downloads the appropriate data files from their [data](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data).

It's all Python3 code, after a recent update.

My database looks like

```
2020-03-22
2020-04-28

Autauga;Alabama;01001;US
0,0,1,4 ...
0,0,0,0 ...

...
``` 

Rather than mark each data point with the date, we just track the first and last dates for the database as a whole.  This means we have to watch for when updates don't happen properly, if a new key appears, or if a county decides not to report after a while.


Options for scripts are:

- the US broken down by states:  ``all_states.py``
- the US broken down by counties:  ``us_by_counties.py``
- a given state broken down by counties:  ``one_state.py``


Features that are currently supported are given by the ``--help`` flag:

```
flags
-h  --help    help
-n     int    display the last n values, default: 7
-N     int    display N rows of data: default: 50
-u     int    data slice ends this many days before yesterday 
(not yet)

-c  --delta   change or delta, display day over day rise
-d  --deaths  display deaths rather than cases (default)
-p  --pop     normalize to population
-r  --rate    compute statistics
-s  --sort    (only if stats are asked for)


example:
python one_state.py [state] -n 10 -sdr

>
```

The statistic is the slope of a linear regression, divided by the mean of the values.  

So, for example, if a 10-day series goes smoothly from 100 to 110, then the slope is about 10/10 = 1 and the statistic is a bit less than 0.01.  If the series goes from 1000 to 1100, then the slope is about 100/10 = 10, but the statistic is still approximately 0.01.

More recently, I have started making what are called choropleth plots, geographic plots where the fill color is based on the statistic for case growth (or whatever else you want).


