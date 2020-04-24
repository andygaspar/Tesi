import numpy as np
import pandas as pd
from itertools import combinations

from Programma.Flight import flight as fl
from Programma.ModelStructure import modelStructure
from Programma.Mip import modelProperties


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

    def __init__(self, df_airline: pd.DataFrame, airline_index, model: modelStructure.ModelStructure):

        self.df = df_airline

        self.name = self.df["airline"].unique()[0]

        self.airline_index = airline_index

        self.num_flights = df_airline.shape[0]

        self.sum_priorities = sum(self.df["priority"])

        self.flights = self.make_airline_flight_list(self.df, model)

        self.flight_pairs = self.pairs(self.flights)

        self.flight_triplets = self.triplet(self.flights)

        self.modelProperties = None

    def set_model_properties(self, mP: modelProperties.ModelProperties):
        self.modelProperties = mP

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
