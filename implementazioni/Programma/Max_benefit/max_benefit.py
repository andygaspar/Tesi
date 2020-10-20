from Programma.ModelStructure import modelStructure as mS
from mip import *
from Programma.ModelStructure.Airline import airline as air
from Programma.ModelStructure.Flight import flight as modFl
from Programma.ModelStructure.Solution import solution

import numpy as np
import pandas as pd

import time


class MaxBenefitModel(mS.ModelStructure):

    def __init__(self, df_init: pd.DataFrame, cost_kind="quadratic", model_name="Max Benefit"):

        self.airlineConstructor = air.Airline
        self.flightConstructor = modFl.Flight
        super().__init__(df_init=df_init, cost_kind=cost_kind)

        self.m = Model(model_name)
        self.x = None
        self.m.threads = -1
        self.m.verbose = 0

    def set_variables(self):
        flight: modFl.Flight
        airline: air.Airline
        self.x = np.array([[self.m.add_var(var_type=BINARY) for k in self.slotIndexes] for flight in self.flights])

    def set_constraints(self):
        flight: modFl.Flight
        airline: air.Airline
        for flight in self.flights:
            self.m += xsum(self.x[flight.num, j] for j in flight.compatible_slots) == 1

        for slot in self.slotIndexes:
            self.m += xsum(self.x[flight.num, slot] for flight in self.flights) <= 1

        for airline in self.airlines:
            self.m += xsum(self.cost_function(flight, flight.slot) for flight in airline.flights) >= \
                      xsum(self.x[flight.num, j] * self.cost_function(flight, j)
                           for flight in airline.flights for j in self.slotIndexes)

    def set_objective(self):
        flight: modFl.Flight
        self.m.objective = minimize(
            xsum(self.x[flight.num, j] * self.cost_function(flight, j)
                 for flight in self.flights for j in self.slotIndexes))

    def run(self):

        self.set_variables()

        start = time.time()
        self.set_constraints()
        end = time.time() - start
        #print("Constraints setting time ", end)

        self.set_objective()

        start = time.time()
        self.m.optimize()
        end = time.time() - start
        #print("Simplex time ", end)

        #print(self.m.status)

        self.mipSolution = self.x

        solution.make_solution(self)
