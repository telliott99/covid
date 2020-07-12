import sys, os, subprocess

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import uinit, udates
import udb, ufile, ukeys, ufmt

def run(src):
    #-------------------------------
    
    # older source files are in subdirectories
    # /Apr, /May etc.
    # those directories are assumed to be complete!
    
    # filter out directories 
    # recent files only
    
    fL = ufile.list_directory(src)
    # here, we need full paths
    src_recent = [src + '/' + fn for fn in fL]
    
    #-------------------------------
    
    # files are named as dates
    date_list = [udates.date_from_path(p) for p in src_recent]
    
    first_all = '2020-03-22'
    first_recent = udates.date_from_path(src_recent[0])
    
        
    all_dates = udates.generate_dates(first=first_recent)
    last = all_dates[-1]
    
    updated = False
    
    for date in all_dates:
        if not date in date_list:
            print('fetch missing data', date)
            ret_code = subprocess.call(['python', "fetch.py", src, date])
            if ret_code != 0:
                print('error in fetch.py')
                sys.exit()
            updated = True
                
    if not updated:
        print('src files up-to-date')
    
#-------------------------------------

def list_src_all(src):
    src_all = []
    todo = []
    
    # distinguish full paths from file/directory names
    # src is a full path
    # so is d
    
    def process_dir(d):
        # os.listdir returns just the file/directory names
        
        dL = os.listdir(d)
        for fn in dL:
            if fn.startswith('.'):
                continue
                
            p = d + '/' + fn
            
            if os.path.isdir(p):
                todo.append(p)
            else:
                if d == src:
                    src_all.append(fn)
                else:
                    # paths without leading '/'
                    d = d.replace(src + '/','')
                    src_all.append(d + '/' + fn)
            
    process_dir(src)
    
    while todo:
        next = todo.pop()
        process_dir(next)
        
        
    def filter(fn):
        if '/' in fn:
            return fn.split('/')[-1]
        return fn
            
    return sorted(src_all, key=filter)
    
