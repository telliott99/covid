import sys, random

N = 2000  # number of persons in the population
meetings_per_day = 20
prob_of_transmission = 0.01
days_infectious = 7
first = 4
last = first + days_infectious
v = len(sys.argv) > 1  # verbose

def roll_dice():
    p = prob_of_transmission
    while True:
        yield random.random() < p

r = roll_dice()
       
class Person:
    def __init__(self, n):
        self.id_num = n 
        self.date_of_infection = None
        self.days_since_infection = None
        self.transmissions = []
        
        # these are updated below
        self.naive = True
        self.presymptomatic = False
        self.infectious = False
        self.recovered = False
        
    def __repr__(self):
        return 'P' + str(self.id_num) + ' '            
        
    def become_infected(self,d):
        self.date_of_infection = d
        self.days_since_infection = 0
        self.naive = False
        self.presymptomatic = True
          
L = [Person(i) for i in range(N)]
L[0].become_infected(0)

# -------------------------

def interact(p1,p2,d):
    if p1.infectious:
        if p2.naive and r.next():
            p1.transmissions.append(p2)
            t = p1.transmissions
            p2.become_infected(d)
            if v:  print p1, 'transmissions: ',
            if v:  print ' '.join([str(p) for p in t])
            
    if p2.infectious: 
        if p1.naive and r.next():
            p2.transmissions.append(p1)
            t = p2.transmissions
            p1.become_infected(d)
            if v:  print p2, 'transmissions: ',
            if v:  print ' '.join([str(p) for p in t])
    
def one_meeting(L,p,d):
    # pick a random other individual
    r = random.choice(L)
    # different than self
    while p == r:
        r = random.choice(L)
    interact(p,r,d)

def one_day(L,p,d):
    for d in range(meetings_per_day):
        one_meeting(L,p,d)

# -------------------------

def update_for_day(L, current_date):
    for p in L:
        if p.naive:
            continue
        value = p.days_since_infection
        d = str(current_date)
        if value == 0:
            if v:  print 'day ' + d, p, 'is presymptomatic'
        if value == first:
            if v:  print 'day ' + d, p, 'is now infectious'
            p.presymptomatic = False
            p.infectious = True
        if value == last:
            if v:  print 'day ' + d, p, 'is now recovered'
            p.infectious = False
            p.recovered = True
        p.days_since_infection += 1

def stats(L):
    nL = [p for p in L if p.naive]
    pL = [p for p in L if p.presymptomatic]
    iL = [p for p in L if p.infectious]
    rL = [p for p in L if p.recovered]
    return len(nL), len(pL), len(iL), len(rL)
    
def mean(L):
    return sum(L) * 1.0 / len(L)

def run(L):
    current_date = 0
    naive, pre, inf, rec = stats(L)
    finished = (naive + rec) == N 
    
    while not finished or current_date < 20:
        if v:  print current_date, stats(L)
        current_date += 1
        update_for_day(L, current_date)
        for p in L:
            one_day(L,p,current_date)
        naive, pre, inf, rec = stats(L)
        finished = (naive + rec) == N
        if finished:  
            return
           
run(L)
naive, pre, inf, rec = stats(L)
print naive, pre, inf, rec

sL = [len(p.transmissions) for p in L if p.recovered]
if v:  print sL
print mean(sL)
