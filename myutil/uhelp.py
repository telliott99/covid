help = '''
flags
-h  --help      help
-n   <int>      display the last -n values, default: 7
-N   <int>      display -N rows of data, default: 50
-c   <int>      --delta, change from x days ago, default: 1
-u   <int>      data slice ends this many days before the last day 

-a  --all       use the complete db, starting 2020-03-22 (default now)
-d  --deaths    display deaths rather than cases (default)
-f  --csv       format output as csv
-o  --only      do not descend from US to states, or states to counties
-p  --pop       normalize to population (disables totals)
-q  --quiet     silence output (for tests)
-r  --rate      compute statistics (over last 7 days)
-s  --sort      
-t  --totals    (only)
-v  --verbose   debugging mode

    --no_dates  suppress dates in row 1
    --counties  show US by counties
    --average   running average (7 days)

to do:

-g  --graph     plot a graph of the data
-m  --map       make a choropleth map

example:
python analyze.py SC -n 10 -sdr

'''
