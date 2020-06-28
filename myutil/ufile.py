import os

def list_directory(d):
    def filter(d,fn):
        return os.path.isdir(d + '/' + fn)    
         
    dL = os.listdir(d)
    dL = [fn for fn in dL if not fn.startswith('.')]   
    dL = [fn for fn in dL if not filter(d,fn)]  
    dL.sort()
    return dL
