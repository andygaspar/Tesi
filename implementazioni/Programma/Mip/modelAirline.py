import numpy as np
import pandas as pd
from itertools import combinations
from Programma.Mip.modelFlight import ModelFlight
from Programma.ModelStructure.Airline import airline as air


class ModelAirline(air.Airline):

    @staticmethod
    def pairs(list_to_comb):
        comb = np.array(list(combinations(list_to_comb, 2)))
        offers = [pair for pair in comb]
        return offers

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def __init__(self, df_airline: pd.DataFrame, airline_index, model):

        super().__init__(df_airline, airline_index, model)

        self.sum_priorities = sum(self.df["priority"])

        self.priorityFunction = model.f

        self.flight_pairs = self.pairs(self.flights)

        self.flight_triplets = self.triplet(self.flights)

        flight: ModelFlight
        for flight in self.flights:
            df_flight = self.df[self.df["flight"] == flight.name]
            flight.set_priority(df_flight["priority"].values[0])
            flight.set_preference(self.sum_priorities, self.priorityFunction)
