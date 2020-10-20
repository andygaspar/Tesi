from typing import Union, Callable, List

import numpy as np
import pandas as pd
from Programma.ModelStructure.modelStructure import ModelStructure
from Programma.UDPP.udppLocal import UDPPlocal
from Programma.UDPP.udppMerge import UDPPmerge
from Programma.ModelStructure.Solution import solution
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flight as fl


class UDPPModel(ModelStructure):

    def __init__(self, df_init: pd.DataFrame, costFun: Union[Callable, List[Callable]]):

        super().__init__(df_init=df_init, costFun=costFun)

        airline: air.Airline
        for airline in self.airlines:
            UDPPlocal(airline, self.slots)

        UDPPmerge(self.flights, self.slots)
        solution.make_solution(self, udpp=True)

    def get_new_df(self):
        self.df: pd.DataFrame
        self.df.reset_index(drop=True, inplace=True)
        self.df["slot"] = self.df["new slot"]
        self.df["gdp schedule"] = self.df["new arrival"]
        return self.df
