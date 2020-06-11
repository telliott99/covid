import scipy.stats as st
import matplotlib.pyplot as plt

SZ = 10000

def uniform(N):
    start = 0
    width = N
    L = list(st.uniform.rvs(size=SZ, 
            loc = start, scale=width))
    return [int(f) for f in L]

def normal(N):
    L = list(st.norm.rvs(size=SZ,loc=0,scale=30))
    L = [abs(n) for n in L if n > 0]
    return L
    
def test_uniform(N):
    L = uniform(N)
    assert min(L) == 0
    assert max(L) == N-1
    return L

def plot(L,N):
    plt.hist(L,bins=N)
    plt.savefig('example.png')
           
if __name__ == "__main__":
    N = 100
    L = test_uniform(N)
    L = normal(N)
    plot(L,N) 
