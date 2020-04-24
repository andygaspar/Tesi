import numpy as np
import pandas as pd
from itertools import combinations
from Programma.Flight import flight as fl


class ModelProperties:

    @staticmethod
    def pairs(list_to_comb):
        return np.array(list(combinations(list_to_comb, 2)))

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def __init__(self, airline, f):

        self.sum_priorities = sum(airline.df["priority"])

        self.priorityFunction = f

        self.flight_pairs = self.pairs(airline.flights)

        self.flight_triplets = self.triplet(airline.flights)

        flight: fl.Flight
        for flight in airline.flights:
            df_flight = airline.df[airline.df["flight"] == flight.name]
            flight.set_priority(df_flight["priority"].values[0])
            flight.set_preference(self.sum_priorities, self.priorityFunction)


