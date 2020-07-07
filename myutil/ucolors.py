import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

L = ['red','blue'] * 50

def get_colors(n):
    return L[:n]
    
cL = ['rgb(0,100,0)',
      'rgb(0,255,0)',
      'rgb(111,255,0)',
      'rgb(255,255,0)',
      'rgb(255,111,0)',
      'rgb(255,0,0)']
