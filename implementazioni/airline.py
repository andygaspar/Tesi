import numpy as np
from itertools import combinations, product
import sys


class Airline:

    @staticmethod
    def pairs(list_to_comb):
        return np.array(list(combinations(list_to_comb, 2)))

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))


    def __init__(self, airline_name, flights, priority, f):
        self.name = airline_name
        self.flights = np.array(flights)
        self.priority= priority
        self.f=f

        self.num_flights = self.flights.shape[0]
        self.sum_priorities = sum(priority)

        for i in range(self.flights.shape[0]):
            flights[i].set_preference(self.num_flights, self.sum_priorities, self.f)

        self.flight_pairs = self.pairs(self.flights)
        self.flight_triplets = self.triplet(self.flights)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
