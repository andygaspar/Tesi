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





