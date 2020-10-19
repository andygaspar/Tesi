import numpy as np
import pandas as pd
import copy
from Programma.UDPP.udppFlight import UDPPFlight
from Programma.ModelStructure.Airline.airline import Airline
from mip import *


class UDPPAirline(Airline):

    def __init__(self, df_airline: pd.DataFrame, airline_index, model):
        super().__init__(df_airline, airline_index, model)

        self.model = model

        self.modelFlightList = None
        self.slotIndexes = model.slotIndexes



        for i in range(len(self.flights)):
            self.flights[i].set_local_num(i)

    def setLocalFlightList(self, flight_list):

        self.modelFlightList = flight_list

    def slot_range(self, k):
        return range(self.AUslots[k].index + 1, self.AUslots[k+1].index)

    def eta_limit(self, flight: UDPPFlight):
        i = 0
        for slot in self.AUslots:
            if slot.index >= flight.eta_slot:
                return i
            i += 1

