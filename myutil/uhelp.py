help = '''
flags
-h  --help     help
-n    <int>    display the last -n values, default: 7
-N    <int>    display -N rows of data, default: 50
-c    <int>    --delta, change from x days ago, default: 1
-L    <int>    depth of search for keys and subkeys, default: 0

-a  --all      use the complete db, starting 2020-03-22
-d  --deaths   display deaths rather than cases (default)
-g  --graph    plot a graph of the data
-m  --map      make a choropleth map
-p  --pop      normalize to population (this disables totals)
-r  --rate     compute statistics (over last 7 days)
-s  --sort     
-t  --totals   (only)
-v  --verbose  debugging mode
-w, --write    text (if -g,-m present, output is normally silent)

to do:
-u   <int>    data slice ends this many days before yesterday 

example:
python %s -n 10 -sdr

'''
