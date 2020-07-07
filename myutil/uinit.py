import sys
from ustates import abbrev_to_state

if sys.argv[0] == "one_state.py":
    extra = '<state>'
elif sys.argv[0] == "country.py":
    extra = '<country>'
else:
    extra = ''

from uhelp import help
help = help % (sys.argv[0], extra)

def bail():
     print(help)
     sys.exit()

def clargs():
    L = sys.argv[1:]
    
    default_dict = { 
      'sys.argv': None,
      'names' : [],
      'deaths': False,       # -d, --deaths
      'mode':'cases', 
      'n':7, 
      'N': False, 
      'upto': 0,
      'regions': None,
      'show_state': False,
      'totals': True,
      
      'all': False,          # -a, --all
      'delta': False,        # -c, --delta
      'graph': False,        # -g, --graph
      'map': False,          # -m, --map
      'pop': False,          # -p, --pop
      'rate': False,         # -r, --rate
      'sort': False,         # -s, --sort
      'total': False,        # -t, --total (only)
      'write': False,        # -w, --write text (when --graph)
      'verbose': False }     # -v, --verbose

#-------------------------------------------
    # no args

    if len(L) == 0:
        return default_dict
        
#-------------------------------------------

    D = default_dict
    L = sys.argv[1:]
    
    if "-h" in L or '--help' in L:
        bail()
                  
    D['sys.argv'] = ' '.join(sys.argv)
    
    # do all args with '--' first
    
    wL = ['deaths',
          'all',
          'delta',
          'graph',
          'map',
          'pop'
          'rate',
          'sort',
          'total',
          'write']
          
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

    # do all args with int modifier
            
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
    # -c can take an int argument 
    # but is different because the int is optional
    # the default value is 1

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

    no_dash = [arg for arg in L if not arg.startswith('-')]
    
    aL = []
    for arg in no_dash:
        try:
            arg = abbrev_to_state[arg]
        except KeyError:
            pass            
        aL.append(arg)
    D['names'] = aL
    
    dash_list = [arg for arg in L if arg.startswith('-')]
    wL = 'dacgmprstvw'
              
    # args may have multiple single-letter values
    fL = []
    for arg in dash_list:
        tmp = arg[1:]
        for f in tmp:
            if not f in wL:
                print('invalid argument: %s' % f)
                bail()
            fL.append(f)
            
#-------------------------------------------
        
    one_letters = ''.join(fL)
    
    if 'd' in one_letters or D['deaths']:
        D['deaths'] = True
        D['mode'] = 'deaths'

    # we allow c to be part of a multi-letter group arg as well
    if not D['delta']:
        if 'c' in one_letters or '--delta' in L:
            D['delta'] = 1
    
    D['all']     = 'a' in one_letters or '--all' in L
    D['map']     = 'm' in one_letters or '--map' in L
    D['graph']   = 'g' in one_letters or '--graph' in L
    D['pop']     = 'p' in one_letters or '--pop' in L
    D['rate']    = 'r' in one_letters or '--rate' in L
    D['sort']    = 's' in one_letters or '--sort' in L
    D['total']   = 't' in one_letters or '--total' in L
    D['verbose'] = 'v' in one_letters or '--verbose' in L
    D['write']   = 'w' in one_letters or '--write' in L
    
    # when -g or -m is selected
    # note: -w, --write is used to control behavior
    # in those two cases, default is silent, no text
                
    return D
