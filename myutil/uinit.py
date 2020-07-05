import sys
from ustates import abbrev_to_state

if sys.argv[0] == "one_state.py":
    extra = '<state>'
elif sys.argv[0] == "country.py":
    extra = '<country>'
else:
    extra = ''

help = '''
flags
-h  --help     help
-n   <int>     display the last -n values, default: 7
-N   <int>     display -N rows of data, default: 50
-u   <int>     window up to -u days ago

-c   <int>     change or delta, default: 1
-d  --deaths   display deaths rather than cases (default)
-m  --max      load the complete db since 2020-03-22
-p  --pop      normalize to population (this disables totals)
-r  --rate     compute statistics (over last 7 days)
-s  --sort     (only if stats are asked for)
-v  --verbose  debugging mode

to do:
-u   <int>    data slice ends this many days before yesterday 

example:
python %s %s -n 10 -sdr
''' % (sys.argv[0], extra)

def bail():
     print(help)
     sys.exit()

def clargs():
    L = sys.argv[1:]
    
    default_dict = { 
      'arg': None,
      'deaths': False,
      'mode':'cases', 
      'n':7, 
      'N': False, 
      'upto': 0,
      
      'max': False,
      'pop': False,
      'sort': False, 
      'stats': False, 
      'delta': False,
      'show_state': False, 
      'totals': True,
      'verbose': False }

#-------------------------------------------
    # no args

    if len(L) == 0:
        return default_dict
        
#-------------------------------------------

    D = default_dict
    L = sys.argv[1:]
    
    if "-h" in L or '--help' in L:
        bail()
                  
    D['args'] = ' '.join(sys.argv[1:])
    
    # do all args with '--' first
    
    wL = ['deaths','max',
          'sort','stats','delta',
          'show_state','totals']
          
    tmp = []
    
#-------------------------------------------

# check -- args for validity

    for arg in L:
        if arg.startswith('--'):
            s = arg[2:]
            if not s in wL:
                print('invalid --arg %s' % s)
                bail()
                
                
    L = [arg for arg in L if not arg.startswith('--')]
                            
#-------------------------------------------

    # now do all args with int modifier
            
    if '-n' in L:
        i = L.index('-n')
        try:
            D['n'] = int(L[i+1])
        except:
            print('-n flag must be followed by an integer value')
            bail()
        L.pop(i+1)
        L.pop(i)
        
    if '-N' in L:
        i = L.index('-N')
        try:
            D['N'] = int(L[i+1])
        except:
            print('-N flag must be followed by an integer value')
            bail()
        L.pop(i+1)
        L.pop(i)
        
    if '-u' in L:
        i = L.index('-u')
        try:
            D['last'] = int(L[i+1])
        except:
            print('-u flag must be followed by an integer value')
            print('(days before yesterday)')
            bail()
        L.pop(i+1)
        L.pop(i)
    
#-------------------------------------------
    # -c is different because we allow an optional int
    # argument to follow

    if '-c' in L:
        i = L.index('-c')
        try:
            j = int(L[i+1])
            L.pop(i+1)
        except (ValueError, IndexError) as e:
            j = 1     
        L.pop(i)
        D['delta'] = j

#-------------------------------------------

    fL = list()
    
    no_dash = [arg for arg in L if not arg.startswith('-')]
    
    if len(no_dash) > 1:
        print('more than one named arg not yet implemented')
        bail()
        
    if len(no_dash) == 1:
        arg = no_dash[0]
        
        # we use full names of states internally
        # to match what db has                            
        try:
            arg = abbrev_to_state[arg]
        except KeyError:
            pass
        D['arg'] = arg
    
    L = [arg for arg in L if arg.startswith('-')]
              
    # args may have multiple single-letter values
    for arg in L:
        tmp = arg[1:]
        for f in tmp:
            if not f in 'cdmprsv':
                print('xinvalid argument %s' % f)
                bail()
            fL.append(f)
            
#-------------------------------------------
        
    one_letters = ''.join(fL)
    
    if 'd' in one_letters or D['deaths']:
        D['deaths'] = True
        D['mode'] = 'deaths'

    # we allow c to be part of a multi-letter group arg as well
    if not D['delta']:
        D['delta']   = 'c' in one_letters or '--delta' in L
    
    D['max']     = 'm' in one_letters or '--max' in L
    D['pop']     = 'p' in one_letters or '--pop' in L
    D['stats']   = 'r' in one_letters or '--stats' in L
    D['sort']    = 's' in one_letters or '--sort' in L
    D['verbose'] = 'v' in one_letters or '--verbose' in L
                
    return D
