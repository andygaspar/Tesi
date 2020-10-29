from typing import Union, Callable, List

import pandas as pd
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.UDPP.LocalOptimised.udppLocalOpt import UDPPlocalOpt
from Programma.UDPP.udppMerge import UDPPmerge
from Programma.ModelStructure.Solution import solution
from Programma.UDPP.AirlineAndFlightAndSlot.udppAirline import UDPPairline
from Programma.UDPP.Local.udppLocal import udpp_local
import time


class UDPPModelOpt(ModelStructure):

    def __init__(self, df_init: pd.DataFrame, costFun: Union[Callable, List[Callable]]):

        super().__init__(df_init=df_init, costFun=costFun, airline_ctor=UDPPairline)

    def run(self, optimised=True):
        airline: UDPPairline
        start = time.time()
        for airline in self.airlines:
            if optimised:
                UDPPlocalOpt(airline, self.slots)
            else:
                udpp_local(airline, self.slots)

        UDPPmerge(self.flights, self.slots)
        print(time.time() - start)
        solution.make_solution(self)
        for flight in self.flights:
            if flight.eta > flight.newSlot.time:
                print("********************** danno UDPP*********************************",
                      flight, flight.eta, flight.newSlot.time)

    def get_new_df(self):
        self.df: pd.DataFrame
        newDf = self.solution.copy(deep=True)
        newDf.reset_index(drop=True, inplace=True)
        newDf["slot"] = newDf["new slot"]
        newDf["fpfs"] = newDf["new arrival"]
        return newDf
