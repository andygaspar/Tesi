from Programma.ModelStructure import modelStructure as mS
from mip import *
from Programma.Amal import amalAirline as air
from Programma.Amal import amalFlight as modFl
from Programma.ModelStructure.Solution import solution

import numpy as np
import pandas as pd

import time


class Amal(mS.ModelStructure):

    def __init__(self, df_init: pd.DataFrame, cost_kind="quadratic", offerMakerFunType="1", model_name="amal"):

        self.airlineConstructor = air.AmalAirline
        self.flightConstructor = modFl.AmalFlight
        self.offerMakerFunType = offerMakerFunType
        super().__init__(df_init=df_init, cost_kind=cost_kind)

        for airline in self.airlines:
            airline.set_offers(self)

        self.m = Model(model_name)
        self.x = []
        self.z = []
        self.y = []
        self.xo = None
        self.m.threads = -1
        self.m.verbose = 0

    def set_variables(self):
        flight: modFl.AmalFlight
        airline: air.AmalAirline
        for flight in self.flights:
            self.x.append([self.m.add_var(var_type=BINARY) for k in flight.classes])

            self.z.append([self.m.add_var(var_type=BINARY) for k in flight.classes])

            self.y.append([self.m.add_var(var_type=BINARY) for j in self.slot_indexes])

    def set_constraints(self):
        flight: modFl.AmalFlight
        airline: air.AmalAirline
        for flight in self.flights:
            self.m += xsum(self.x[flight.num][k] for k in range(len(flight.classes))) == 1

        for flight in self.flights:
            self.m += self.x[flight.num][0] + self.z[flight.num][0] - \
                      xsum(self.y[flight.num][j] for j in flight.class_range(0)) == 0

        for flight in self.flights:
            for k in range(1, len(flight.classes)):
                self.m += self.x[flight.num][k] + self.z[flight.num][k] - self.z[flight.num][k-1] - \
                          xsum(self.y[flight.num][j] for j in flight.class_range(k)) == 0

        for j in self.slot_indexes:
            self.m += xsum(self.y[flight.num][j] for flight in self.flights) == 1

    def set_objective(self):
        flight: modFl.AmalFlight
        self.m.objective = minimize(
            xsum(self.y[flight.num][j] * self.cost_function(flight, j)
                 for flight in self.flights for j in self.slot_indexes))

    def run(self):

        self.set_variables()

        start = time.time()
        self.set_constraints()
        end = time.time() - start
        print("Constraints setting time ", end)

        self.set_objective()

        start = time.time()
        self.m.optimize()
        end = time.time() - start
        print("Simplex time ", end)

        print(self.m.status)

        self.mipSolution = self.y

        solution.make_solution(self)



