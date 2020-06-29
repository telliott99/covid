import sys
from ustrings import abbrev_to_state

if sys.argv[0] == "one_state.py":
    extra = '[state]'
else:
    extra = ''

help = '''
flags
-h  --help    help
-n   <int>    display the last n values, default: 7
-N   <int>    display N rows of data: default: 50

-c  --delta   change or delta, display day over day rise
-d  --deaths  display deaths rather than cases (default)
-m  --max     load the complete db since 2020-03-22
-r  --rate    compute statistics
-s  --sort    (only if stats are asked for)

to do:
-u   <int>    data slice ends this many days before yesterday 
-p  --pop     normalize to population

example:
python %s %s -n 10 -sdr
''' % (sys.argv[0], extra)

def clargs():
    try:
        L = sys.argv[1:]
    except NameError:
        import sys
        L = sys.argv[1:]
        
    sL = [arg for arg in L if arg.startswith('-') and not arg.startswith('--')]
    one_letters = ''.join(sL)
    
    if "h" in one_letters or '--help' in L:
        print(help)
        sys.exit()
        
    D = { 'mode':'cases', 'n':7, 'N': 100, 'upto': 0,
          'sort': False, 'stats': False, 'delta': False }
          
    if len(sys.argv) > 1:
        D['args'] = ' '.join(sys.argv[1:])
    
    if 'd' in one_letters or '--deaths' in L:
        D['mode'] = 'deaths'
        
    if '-n' in L:
        i = L.index('-n')
        try:
            D['n'] = int(L[i+1])
        except:
            print('-n flag must be followed by an integer value')
            sys.exit()
        L.pop(i+1)
        L.pop(i)
        
    if '-N' in L:
        i = L.index('-N')
        try:
            D['N'] = int(L[i+1])
        except:
            print('-n flag must be followed by an integer value')
            sys.exit()
        L.pop(i+1)
        L.pop(i)
        
    if '-u' in L:
        i = L.index('-u')
        try:
            D['last'] = int(L[i+1])
        except:
            print('-u flag must be followed by an integer value')
            print('(days before yesterday)')
            sys.exit()
        L.pop(i+1)
        L.pop(i)
    
    
    D['totals'] = True
        
    D['sort']  = 's' in one_letters or '--sort' in L
    D['stats'] = 'r' in one_letters or '--rate' in L
    D['delta'] = 'c' in one_letters or '--delta' in L
    D['max']   = 'm' in one_letters or '--max' in L
        
    L = [arg for arg in L if not arg.startswith('-')]
    if len(L) > 0:
        arg = L[0]
        try:
            arg = abbrev_to_state[arg]
        except KeyError:
            pass
        D['arg'] = arg
    else:
        D['arg'] = None
        
    # we use full names of states internally, b/c that's what db has
                
    return D
