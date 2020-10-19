import numpy as np
import pandas as pd
from itertools import product
from Programma.ModelStructure.Slot import slotList as sl
from Programma.ModelStructure.Airline import airline as air


class ModelStructure:

    def compute_delays(self):
        delays = np.zeros((self.slotIndexes.shape[0], self.slotIndexes.shape[0]))
        for flight, j in product(self.flights, self.slotIndexes):
            delays[flight.num, j] = (self.slotTimeGrid[j] - flight.eta)

        delays = np.where(delays < 0, 0, delays)
        return delays

    @staticmethod
    def delay_cost(flight, delay):
        return (flight.cost * delay ** 2)/2

    def __init__(self, df_init: pd.DataFrame, cost_kind: str):

        self.df = df_init

        self.slotIndexes = self.df["slot"].to_numpy()

        self.slotTimeGrid = self.df["gdp schedule"].to_numpy()

        self.slots = sl.make_slots_list(self.df)

        from Programma.ModelStructure.Flight import flightList as fll
        from Programma.ModelStructure.Airline import airlineList as airList

        self.cost_kind = cost_kind

        self.airlines = airList.make_airlines_list(self.df, self.slots)

        self.num_airlines = len(np.unique(self.df["airline"]))

        self.flights = fll.make_flight_list(self)

        #fll.assign_flight_num(self.flights)

        self.num_flights = len(self.flights)

        self.delays = self.compute_delays()

        self.initial_total_costs = self.compute_costs(self.flights, "initial")

        self.empty_slots = self.df[self.df["flight"] == "Empty"]["slot"].to_numpy()

        self.mipSolution = None

        self.solution_array = None

        self.solution = None

        self.solutionDf = None

        self.report = None

    def cost_function(self, flight, slot):
        from Programma.ModelStructure.Costs.costs import cost_function as cf
        return cf(self, flight, slot)

    def compute_costs(self, flights, which):
        if which == "initial":
            return sum([self.cost_function(flight, flight.slot) for flight in flights])
        if which == "final":
            return sum([self.cost_function(flight, flight.newSlot) for flight in flights])

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


