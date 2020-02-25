import numpy as np
from itertools import combinations

import flight as fl


class Airline:

    @staticmethod
    def pairs(list_to_comb):
        return np.array(list(combinations(list_to_comb, 2)))

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def make_airline_flight_list(self,df_airline,model):
        flight_list = []
        for i in range(df_airline.shape[0]):
            line = df_airline.iloc[i]
            flight_list.append(fl.Flight(line,self,model))

        return np.array(flight_list)

    def __init__(self, df_airline, airline_index, model):

        self.name = df_airline["airline"].unique()[0]

        self.airline_index = airline_index

        self.num_flights = df_airline.shape[0]

        self.sum_priorities = sum(df_airline["priority"])

        self.flights = self.make_airline_flight_list(df_airline,model)

        self.flight_pairs = self.pairs(self.flights)

        self.flight_triplets = self.triplet(self.flights)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
