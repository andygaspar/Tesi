import numpy as np
from mip import *
import string
from itertools import combinations, product
import sys


def pairs(list_to_comb):
    return np.array(list(combinations(list_to_comb, 2)))


def triplet(list_to_comb):
    return np.array(list(combinations(list_to_comb, 3)))


class Airline:

    @staticmethod
    def f_names(flights):
        flights_name = []
        for f in flights:
            flights_name.append(string.ascii_uppercase[f])
        return flights_name

    @staticmethod
    def preference_function(priority, f):
        return priority * f(len(priority)) / sum(priority)

    def __init__(self, airline_name, flights, priority, f_names=0, costs=[], f=lambda x: x):
        self.name = airline_name
        self.flights = np.array(flights)

        if f_names == 0:
            self.flights_name = dict(zip(self.flights, self.f_names(flights)))
        else:
            self.flights_name = f_names

        self.priority = np.array(priority)
        if len(costs) == 0:
            self.costs = dict(zip(self.flights, self.f_names(flights)))
        else:
            self.costs = dict(zip(self.flights,costs))
        self.preferences_list = self.preference_function(self.priority, f)
        self.preferences = dict(zip(self.flights, self.preferences_list))

        self.flight_pairs = pairs(self.flights)
        self.flight_triplets = triplet(self.flights)

    def set_preferences(self, f):
        self.preferences_list = f(self.priority)
        self.preferences = dict(zip(self.flights, self.preferences_list))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
