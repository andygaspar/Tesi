import numpy as np
import pandas as pd
from itertools import combinations

from Programma.Flight import flight as fl
#from Programma.Mip.modelProperties import ModelProperties
from Programma.ModelStructure.modelStructure import ModelStructure


class Airline:

    @staticmethod
    def pairs(list_to_comb):
        return np.array(list(combinations(list_to_comb, 2)))

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def make_airline_flight_list(self, df_airline, model):
        flight_list = []
        for i in range(df_airline.shape[0]):
            line = df_airline.iloc[i]
            flight_list.append(fl.Flight(line, self, model))

        return np.array(flight_list)

    def __init__(self, df_airline: pd.DataFrame, airline_index, model: ModelStructure):

        self.df = df_airline

        self.name = self.df["airline"].unique()[0]

        self.airline_index = airline_index

        self.num_flights = df_airline.shape[0]

        self.sum_priorities = sum(self.df["priority"])

        self.flights = self.make_airline_flight_list(self.df, model)

        self.flight_pairs = self.pairs(self.flights)

        self.flight_triplets = self.triplet(self.flights)

        self.modelProperties = None

        self.amalProperties = None

    def set_model_properties(self, mP):
        self.modelProperties = mP

    def set_amal_properties(self, amalProperties):
        self.amalProperties = amalProperties

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
