import sys

def clargs():
    try:
        L = sys.argv[1:]
    except NameError:
        import sys
        L = sys.argv[1:]
    D = { 'mode':'cases', 'n':7, 'N': 100 }
    if '-d' in L:
        D['mode'] = 'deaths'
    if '-n' in L:
        i = L.index('-n')
        D['n'] = int(L[i+1])
    if '-N' in L:
        i = L.index('-N')
        D['N'] = int(L[i+1])
    D['arg'] = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if not arg.startswith('-'):
            D['arg'] = arg
    return D
