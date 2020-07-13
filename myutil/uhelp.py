help = '''
flags
-h  --help      help
-n    <int>     display the last -n values, default: 7
-N    <int>     display -N rows of data, default: 50
-c    <int>     --delta, change from x days ago, default: 1

-a  --all       use the complete db, starting 2020-03-22
-d  --deaths    display deaths rather than cases (default)
-f  --csv       format output as csv
-o  --only      do not descend from say, US to states
-p  --pop       normalize to population (this disables totals)
-q  --quiet     silence output (for tests)
-r  --rate      compute statistics (over last 7 days)
-s  --sort      
-t  --totals    (only)
-v  --verbose   debugging mode

    --no_dates  suppress dates in row 1
    --counties  show US by counties

to do:
-g  --graph     plot a graph of the data
-m  --map       make a choropleth map
-u   <int>      data slice ends this many days before yesterday 

example:
python %s -n 10 -sdr

'''
