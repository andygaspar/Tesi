import numpy as np
import pandas as pd
from typing import Union, List, Callable
from itertools import product
from Programma.ModelStructure.Slot import slotList as sl
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flightList as fll
from Programma.ModelStructure.Airline import airlineList as airList


class ModelStructure:

    def __init__(self, df_init: pd.DataFrame, costFun: Union[Callable, List[Callable]]):

        self.df = df_init

        self.slotIndexes = self.df["slot"].to_numpy()

        self.slotTimeGrid = self.df["gdp schedule"].to_numpy()

        self.slots = sl.make_slots_list(self.df)

        self.airlines = airList.make_airlines_list(self.df, self.slots)

        self.numAirlines = len(np.unique(self.df["airline"]))

        self.flights = fll.make_flight_list(self)

        self.set_flights_cost_functions(costFun)

        self.numFlights = len(self.flights)

        self.initialTotalCosts = self.compute_costs(self.flights, "initial")

        self.emptySlots = self.df[self.df["flight"] == "Empty"]["slot"].to_numpy()

        self.mipSolution = None

        self.solutionArray = None

        self.solution = None

        self.solutionDf = None

        self.report = None

    @staticmethod
    def compute_costs(flights, which):
        if which == "initial":
            return sum([flight.costFun(flight, flight.slot) for flight in flights])
        if which == "final":
            return sum([flight.costFun(flight, flight.newSlot) for flight in flights])

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def print_schedule(self):
        print(self.df)

    def print_solution(self):
        print(self.solutionDf)

    def get_flight_by_slot_index(self, i):
        for flight in self.flights:
            if flight.slot == i:
                return flight

    def get_flight_name(self, f_name):
        for flight in self.flights:
            if flight.name == f_name:
                return flight

    def find_match(self, i):
        for j in self.slotIndexes[self.slotIndexes != i]:
            if self.mipSolution[i.slot, j] == 1:
                return self.flights[j]

    def set_flights_cost_functions(self, costFun):
        if isinstance(costFun, Callable):
            for flight in self.flights:
                flight.set_cost_fun(costFun)
        else:
            i = 0
            for flight in self.flights:
                flight.set_cost_fun(costFun[i])
                i += 1
