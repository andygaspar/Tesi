from typing import List

import numpy as np
import pandas as pd
from itertools import combinations
from Programma.UDPP.AirlineAndFlightAndSlot.udppFlight import UDPPflight
from Programma.ModelStructure.Airline import airline as air


class UDPPairline(air.Airline):

    flights: List[UDPPflight]

    @staticmethod
    def pairs(list_to_comb):
        comb = np.array(list(combinations(list_to_comb, 2)))
        offers = comb #[pair for pair in comb if np.abs(pair[0].priority-pair[1].priority) > 0.2]
        return offers

    @staticmethod
    def triplet(list_to_comb):
        return np.array(list(combinations(list_to_comb, 3)))

    def __init__(self, df_airline: pd.DataFrame, airline_index, slots):

        super().__init__(df_airline=df_airline, airline_index=airline_index, slots=slots, flight_ctor=UDPPflight)

        self.check_tna()

        self.agent = None

    def check_tna(self):
        for flight in self.flights:
            if flight.tna < self.flights[0].slot.time:
                flight.tna = self.flights[0].slot.time

