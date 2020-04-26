from Programma.ModelStructure import modelStructure as mS
from mip import *
from Programma.Amal import amalAirline as air
from Programma.Amal import amalFlight as modFl

import numpy as np
import pandas as pd

import time


class Amal(mS.ModelStructure):

    @staticmethod
    def index(array, elem):
        for i in range(len(array)):
            if np.array_equiv(array[i], elem):
                return i

    @staticmethod
    def get_tuple(flight):
        j = 0
        indexes = []
        for pair in flight.airline.flight_pairs:
            if flight in pair:
                indexes.append(j)
            j += 1
        return indexes

    def __init__(self, df_in: pd.DataFrame, kind="1", model_name="amal"):

        self.airlineConstructor = air.AmalAirline
        self.flightConstructor = modFl.AmalFlight
        self.kind = kind
        super().__init__(df_in)

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

        self.solution_array = self.make_solution_array(self.y)

        print(self.solution_array)

        for i in range(self.solution_array.shape[0]):
            flight = self.get_flight_by_slot_index(i)
            if flight is not None:
                new_slot = np.argwhere(self.solution_array[i] == 1)[0][0]
                if new_slot == flight.slot:
                    print(flight, new_slot)
                else:
                    print(flight, new_slot, flight.slot)

        # self.solution = sol.Solution(self)

    def make_solution_array(self, x):
        solution_array = np.zeros((self.slot_indexes.shape[0], self.slot_indexes.shape[0]))
        for flight in self.flights:
            for j in range(len(x[flight.num])):
                solution_array[flight.slot, j] = x[flight.num][j].x
        return solution_array
