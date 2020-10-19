import numpy as np
import pandas as pd
from itertools import combinations

from Programma.ModelStructure.modelStructure import ModelStructure


class Airline:

    def make_airline_flight_list(self, model):
        flight_list = []
        for i in range(self.df.shape[0]):
            line = self.df.iloc[i]
            flight_list.append(model.flightConstructor(line, self, model))

        return np.array(flight_list)

    def __init__(self, df_airline: pd.DataFrame, airline_index, model: ModelStructure):

        self.df = df_airline

        self.name = self.df["airline"].unique()[0]

        self.index = airline_index

        self.num_flights = df_airline.shape[0]

        self.flights = self.make_airline_flight_list(model)

        #self.initialCosts = sum([flight.cost for flight in self.flights])
        self.AUslots = np.array([flight.slot for flight in self.flights])

        self.finalCosts = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
