import numpy as np
import pandas as pd
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.UDPP.udppLocal import UDPPlocal
from Programma.UDPP.udppMerge import UDPPmerge
from Programma.ModelStructure.Solution import solution
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flight as fl


class UDPPModel(ModelStructure):

    def __init__(self, df_init: pd.DataFrame, cost_kind: str ="quadratic"):

        super().__init__(df_init=df_init, cost_kind=cost_kind)

        airline: air.Airline
        for airline in self.airlines:
            UDPPlocal(airline, self.slots)

        UDPPmerge(self.flights, self.slots)
        flight: fl.Flight
        df_UDPP: pd.DataFrame


        # UDPP_solution = [flight.UDPPlocalSolution.index for flight in self.flights]
        # self.df["UDPPpremerge"] = UDPP_solution
        # df_UDPP = self.df.sort_values(by=["UDPPpremerge", "eta"])
        #
        # for i in range(df_UDPP.shape[0]):
        #     line = df_UDPP.iloc[i]
        #     flight = self.get_flight_name(line["flight"])
        #     if i < flight.eta_slot:
        #         print("************************************", flight, i, " earlier than eta")
        #     flight.newSlot = self.slots[i]
        #     flight.new_arrival =  flight.newSlot.time #self.gdp_schedule[i]


        solution.make_solution(self, udpp=True)

    def get_new_df(self):
        self.df: pd.DataFrame
        self.df.reset_index(drop=True, inplace=True)
        self.df["slot"] = self.df["new slot"]
        self.df["gdp schedule"] = self.df["new arrival"]
        return self.df
