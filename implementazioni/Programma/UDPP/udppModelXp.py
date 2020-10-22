from typing import Union, Callable, List

import numpy as np
import pandas as pd
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.UDPP.udppLocalXpress import UDPPlocalXpress
from Programma.UDPP.udppMerge import UDPPmerge
from Programma.ModelStructure.Solution import solution
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flight as fl

import time

class UDPPModelXp(ModelStructure):

    def __init__(self, df_init: pd.DataFrame, costFun: Union[Callable, List[Callable]]):

        super().__init__(df_init=df_init, costFun=costFun)

        airline: air.Airline
        start = time.time()
        for airline in self.airlines:
            UDPPlocalXpress(airline, self.slots)

        UDPPmerge(self.flights, self.slots)
        print(time.time() - start)
        solution.make_solution(self)


    def get_new_df(self):
        self.df: pd.DataFrame
        newDf = self.solution.copy(deep=True)
        newDf.reset_index(drop=True, inplace=True)
        newDf["slot"] = newDf["new slot"]
        newDf["fpfs"] = newDf["new arrival"]
        return newDf
