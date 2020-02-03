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
