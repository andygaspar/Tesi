from typing import Callable

import numpy as np
import pandas as pd
from itertools import combinations
from Programma.Istop.istopFlight import IstopFlight
from Programma.ModelStructure.Airline import airline as air


class IstopAirline(air.Airline):

    @staticmethod
    def pairs(list_to_comb):
        comb = np.array(list(combinations(list_to_comb, 2)))
        offers = comb #[pair for pair in comb if np.abs(pair[0].priority-pair[1].priority) > 0.2]
        return offers

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def __init__(self, df_airline: pd.DataFrame, airline_index, slots):

        super().__init__(df_airline=df_airline, airline_index=airline_index, slots=slots, flight_ctor=IstopFlight)

        self.sum_priorities = sum(self.df["priority"])

        self.flight_pairs = self.pairs(self.flights)

        self.flight_triplets = self.triplet(self.flights)

    def set_preferences(self, priorityFunction):
        flight: IstopFlight
        for flight in self.flights:
            df_flight = self.df[self.df["flight"] == flight.name]
            flight.set_priority(df_flight["priority"].values[0])
            flight.set_preference(self.sum_priorities, priorityFunction)
