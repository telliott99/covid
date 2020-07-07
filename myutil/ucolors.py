import sys, os
base = os.environ.get('covid_base')
sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

L = ['red','blue'] * 50

def get_colors(n):
    return L[:n]