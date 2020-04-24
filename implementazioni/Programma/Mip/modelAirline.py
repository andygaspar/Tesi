import numpy as np
import pandas as pd
from itertools import combinations
from Programma.Flight import flight as fl
from Programma.Airline import airline as air


class ModelAirline(air.Airline):

    @staticmethod
    def pairs(list_to_comb):
        return np.array(list(combinations(list_to_comb, 2)))

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def __init__(self, airline: air.Airline, f):

        self.sum_priorities = sum(airline.df["priority"])

        self.priorityFunction = f

        self.flight_pairs = self.pairs(airline.flights)

        self.flight_triplets = self.triplet(airline.flights)


