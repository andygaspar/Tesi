from typing import Union, Callable, List

import numpy as np
import pandas as pd
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.UDPP.udppLocalOpt import UDPPlocalOpt
from Programma.UDPP.udppLocalOptTest import UDPPlocalOptTest
from Programma.UDPP.udppMerge import UDPPmerge
from Programma.ModelStructure.Solution import solution
from Programma.ModelStructure.Airline import airline as air

import time


class UDPPModelOpt(ModelStructure):

    def __init__(self, df_init: pd.DataFrame, costFun: Union[Callable, List[Callable]]):

        super().__init__(df_init=df_init, costFun=costFun)

        airline: air.Airline
        start = time.time()
        for airline in self.airlines:
            UDPPlocalOptTest(airline, self.slots)

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
