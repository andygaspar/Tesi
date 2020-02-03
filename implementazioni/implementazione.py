import numpy as np
from mip import *
import string
from itertools import combinations,product
import sys





def pairs(list_to_comb):
    return np.array(list(combinations(list_to_comb,2)))

def triplet(list_to_comb):
    return np.array(list(combinations(list_to_comb,3)))

class airline:

    def f_names(self,flights):
        flights_name=[]
        for f in flights:
            flights_name.append(string.ascii_uppercase[f])
        return flights_name

    def preference_function(self,priority,f):
        return priority*f(len(priority))/sum(priority)


    def __init__(self,name,flights,priority,f=lambda x: x):
        self.name=name
        self.flights=np.array(flights)
        self.flights_name=dict(zip(self.flights,self.f_names(flights)))

        self.priority=np.array(priority)
        self.preferences_list=self.preference_function(self.priority,f)
        self.preferences=dict(zip(self.flights,self.preferences_list))

        self.flight_pairs=pairs(self.flights)
        self.flight_triplets=triplet(self.flights)


    def set_preferencies(self,f):
        self.preferences_list=f(self.priority)
        self.preferences=dict(zip(self.flights,self.preferences_list))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class model:

    def compute_delays(self):
        delays=np.zeros((self.num_flights,self.num_flights))
        for i,j in product(self.slots,self.slots):
            delays[i,j]=self.FPFS[j]-self.ETA[i]
        return delays

    def compute_ETA_index(self,ETA):
        ETA_index=[]
        for i in ETA:
            j=0
            while j<len(ETA) and self.FPFS[j]<i:
                j+=1
            ETA_index.append(j)
        return ETA_index

    def __init__(self,airlines,ETA,FPFS_scheduling,model_name="model",f=lambda x: x):

        self.e=sys.float_info.min

        self.num_flights=len(ETA)
        self.num_airlines=len(airlines)
        self.airlines=np.array(airlines)

        self.ETA=np.array(ETA)
        self.FPFS=np.array(FPFS_scheduling)
        self.ETA_index=self.compute_ETA_index(self.ETA)

        self.slots=np.array([i for i in range(len(self.FPFS))])
        self.delays=self.compute_delays()
        for a in self.airlines:
            a.set_preferencies(f)

        self.new_schedule=[]
        self.solution=None
        self.m= Model(model_name)

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def score(self,airline,i,j):
        return self.delays[i,j]*airline.preferences[i]

    def which_airline(self,flight):
        for a in self.airlines:
            if flight in a.flights:
                return a
    def get_flights_name(self,i):
        return self.which_airline(i).flights_name[i]

    def print_schedule(self):
        print("{0:^10}".format("AIRLINE"),"{0:^10}".format("FLIGTH"),\
        "{0:^10}".format("ETA"),"{0:^10}".format("DELAY"),"{0:^10}".format("COSTS"))

        for i in self.slots:
            print("{0:^10}".format(str(self.which_airline(i))),\
            "{0:^10}".format(self.which_airline(i).flights_name[i]),\
            "{0:^10}".format(self.ETA[i]),\
            "{0:^10}".format(self.delays[i,i]),\
            "{0:^10}".format(self.which_airline(i).preferences[i]*self.delays[i,i]))

    def print_solution(self):
        print("{0:^10}".format("AIRLINE"),"{0:^10}".format("FLIGTH"),\
        "{0:^10}".format("ETA"),"{0:^10}".format("DELAY"),"{0:^10}".format("COSTS"))

        for sol in self.new_schedule:
            print("{0:^10}".format(str(self.which_airline(sol[0]))),\
            "{0:^10}".format(self.which_airline(sol[0]).flights_name[sol[0]]),\
            "{0:^10}".format(self.ETA[sol[0]]),\
            "{0:^10}".format(self.delays[sol[0],sol[1]]),\
            "{0:^10}".format(self.which_airline(sol[0]).preferences[sol[0]]*self.delays[sol[0],sol[1]]))

    def print_offers(self):
        for i,j in product(self.slots,self.slots):
            if i<j and self.solution[i,j].x!=0:
                print("(",self.which_airline(i),",",self.get_flights_name(i),") x ("\
                ,self.which_airline(j),",",self.get_flights_name(j),")")


class model_1(model):

    def __init__(self,airlines,ETA,FPFS_scheduling,f=lambda x: x):
        super().__init__(airlines,ETA,FPFS_scheduling,f=lambda x: x)


    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

        for i in range(len(self.slots)):
            self.m += xsum(x[i,j] for j in self.slots) == 1

        for j in range(len(self.slots)):
            self.m += xsum(x[i,j] for i in self.slots) <= 1

        for i,j in product(self.slots,self.slots):
            if j<self.ETA_index[i]:
                self.m+= x[i,j]==0

        for i,j in product(self.slots,self.slots):
            self.m += x[i,j]==x[j,i]

        for v in self.airlines:
            for w in self.airlines:
                if v.name!=w.name:
                    self.m += xsum(x[i,j] * self.score(v,i,j) for i in v.flights for j in w.flights) <= \
                    xsum(x[i,j] * self.score(v,i,i) for i in v.flights for j in w.flights)-self.e

        self.m.objective= minimize(xsum(x[i,j]*self.score(a,i,j) for a in self.airlines for i in a.flights for j in self.slots))

        self.m.optimize()
        self.solution=x

        for j in self.slots:
            for i in self.slots:
                if x[i,j].x!=0:
                    self.new_schedule.append((i,j))

class model_2(model):

    def __init__(self,airlines,ETA,FPFS_scheduling,f=lambda x: x):
        super().__init__(airlines,ETA,FPFS_scheduling,f=lambda x: x)
        self.airlines_pairs=pairs(self.airlines)
        self.c = np.array([[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])
        self.x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

        c = np.array([[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])
        print(c)

        for i in range(len(self.slots)):
            self.m += xsum(x[i,j] for j in self.slots) == 1

        for j in range(len(self.slots)):
            self.m += xsum(x[i,j] for i in self.slots) <= 1


        for air_pair in self.airlines_pairs:
            airlineA=air_pair[0].flight_pairs
            airlineB=air_pair[1].flight_pairs
            for pairA in airlineA:
                for pairB in airlineB:
                    self.m += xsum(x[i,j] for i in pairA for j in pairB) + xsum(x[j,i] for i in pairA for j in pairB)\
                     <= (c[ind(problem.airlines,air_pair[0])][ind(airlineA,pairA)] \
                     + c[np.where(problem.airlines == air_pair[1])][np.where(airlineB == pairB)])*2

                    self.m += xsum(x[i,j] * self.score(air_pair[0],i,j) for i in pairA for j in pairB) <= \
                    xsum(x[i,j] * self.score(v,i,i) for i in pairA for j in pairB)-self.e


        self.m.objective= minimize(xsum(x[i,j]*self.score(a,i,j) for a in self.airlines for i in a.flights for j in self.slots))

        self.m.optimize()
        self.solution=x

        for j in self.slots:
            for i in self.slots:
                if x[i,j].x!=0:
                    self.new_schedule.append((i,j))


def ind(array,elem):
    return np.where(array == elem)[0]


BA=airline("BA",[1,4,5],[4,9,12])
YA=airline("YA",[0,2,3,6],[1,14,1,15])

ETA=np.array(range(7))
FPFS=ETA*2

problem=model_2([BA,YA],ETA,FPFS)
problem.x
problem.c[0][0]
problem.run()


c = np.array([[i for i in airline.flight_pairs] for airline in problem.airlines])
for i in c:
    print(i)









problem.run()

problem.print_schedule()
problem.print_solution()
problem.print_offers()
