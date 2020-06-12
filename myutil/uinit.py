import sys

if sys.argv[0] == "one_state.py":
    extra = '[state]'
else:
    extra = ''

help = '''
flags
-h --help    help
-n    int    display the last n values, default: 7
-N    int    display N rows of data: default: 50
-d --deaths  display deaths rather than cases (default)
-r --rate    compute statistics
-s --sort    (only if stats are asked for)
-c --delta   change or delta, display day over day rise, not yet implemented

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
        print help
        sys.exit()
        
    D = { 'mode':'cases', 'n':7, 'N': 100,
          'sort': False, 'stats': False, 'delta': False }
    
    if 'd' in one_letters or '--deaths' in L:
        D['mode'] = 'deaths'
        
    if '-n' in L:
        i = L.index('-n')
        D['n'] = int(L[i+1])
        L.pop(i+1)
        L.pop(i)
        
    if '-N' in L:
        i = L.index('-N')
        D['N'] = int(L[i+1])
        L.pop(i+1)
        L.pop(i)
    
    D['totals'] = True
        
    if 's' in one_letters or '--sort' in L:
        D['sort'] = True
    
    if 'r' in one_letters or '--rate' in L:
        D['stats'] = True

    if 'c' in one_letters or '--delta' in L:
        D['delta'] = True
        
    L = [arg for arg in L if not arg.startswith('-')]
    if len(L) > 0:
        D['arg'] = L[0]
    else:
        D['arg'] = None
        
    return D
