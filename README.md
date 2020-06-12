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

Options for scripts are:

- the US broken down by states:  ``all_states.py``
- the US broken down by counties:  ``us_by_counties.py``
- a given state broken down by counties:  ``one_state.py``


Features that are currently supported are given by the ``--help`` flag:

```
> python all_states.py -h           

flags
-h --help    help
-n    int    display the last n values, default: 7
-N    int    display N rows of data: default: 50
-d --deaths  display deaths rather than cases (default)
-r --rate    compute statistics
-s --sort    (only if stats are asked for)
-c --delta   change or delta, display day over day rise

example:
python all_states.py  -n 10 -sdr

>
```
