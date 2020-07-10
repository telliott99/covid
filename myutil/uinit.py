import sys
import ustates
from ustates import abbrev_to_state
from ufmt import pprint


from uhelp import help
help = help % (' '.join(sys.argv))

def bail():
     print(help)
     sys.exit()

def clargs():
    L = sys.argv[1:]
    
    default_dict = { 
      'sys.argv': None,
      'names' : [],
      'deaths': False,   # -d, --deaths
      'mode':'cases', 
      'n':7, 
      'N': False,
      'show_parent_label': False,
      'add_totals': True,
      
      'all': False,      # -a, --all
      'delta': False,    # -c, --delta
      #'graph': False,    # -g, --graph
      #'map': False,      # -m, --map
      'only': False,     # -o, --only, no states
      'pop': False,      # -p, --pop
      'quiet': False,    # -q, --quiet, for testing
      'rate': False,     # -r, --rate
      'sort': False,     # -s, --sort
      'verbose': False } # -v, --verbose
            
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
    
#-------------------------------------------

    # do all args with '--' first
    
    wL = ['deaths',
          'all',
          'delta',
          'graph',
          'map',
          'pop',
          'quiet',
          'rate',
          'sort',
          'total']
          
    tmp = []
    
    # check -- args for validity but don't set yet
    
    for arg in L:
        if arg.startswith('--'):
            s = arg[2:]
            if not s in wL:
                print('--%s is not a valid argument' % s)
                bail()
                                            
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
    
#-------------------------------------------

    # -c can take an int argument 
    # but it's different because the int is optional
    # default value is 1

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
        if arg == 'us':
            arg = 'US'
        # allow states to be lower case
        cap = arg.upper()
        if cap in ustates.abbrev:
            arg = abbrev_to_state[cap] 
        aL.append(arg)
        
    D['names'] = aL
    
    dash_list = []
    for arg in L:
        if arg.startswith('-') and not arg[1] == '-':
            dash_list.append(arg)

    wL = 'dacgmopqrsvw'
              
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
    D['quiet']   = 'q' in one_letters or '--quiet' in L
    D['rate']    = 'r' in one_letters or '--rate' in L
    D['sort']    = 's' in one_letters or '--sort' in L
    D['verbose'] = 'v' in one_letters or '--verbose' in L
    
    D['only']    = 'o' in one_letters or '--only' in L
    if D['only']:
        D['add_totals'] = False
        
    if 'eu' in D['names'] and D['only']:
        print('-o option not available for eu')
        sys.exit()
  
    # when -g or -m is selected
    # note: -q, --quiet is used to control behavior
    # in those two cases, default is silent, no text
    
    return D
