from Programma.Airline import airline as al
from Programma.ModelStructure import modelStructure as mS
from mip import *
from Programma.Solution import solution as sol
from Programma.Airline import airline as air
from Programma.Amal import amalProperties

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

    def __init__(self, df_in: pd.DataFrame, kind: str, model_name="amal"):

        super().__init__(df_in, model_name)

        self.m = Model(model_name)
        self.x = []
        self.z = []
        self.y = []
        self.xo = None
        self.m.threads = -1
        self.m.verbose = 0

        airline: air.Airline
        for airline in self.airlines:
            airline.set_amal_properties(amalProperties.AmalProperties(kind, airline.df))

    def set_variables(self):

        for flight in self.flights:
            self.x.append([self.m.add_var(var_type=BINARY) for k in flight.airline.getOffersForFlight(flight)])

            self.z.append([self.m.add_var(var_type=BINARY) for k in flight.airline.getOffersForFlight(flight)])

            self.y.append([self.m.add_var(var_type=BINARY) for j in self.slot_indexes])

    def set_constraints(self):

        for flight in self.flights:
            self.m += xsum(self.x[flight.slot][k] for k in range(len(flight.airline.getOffersForFlight(flight)))) == 1

        for flight in self.flights:
            self.m += self.x[flight.slot][0] + self.z[flight.slot][0] - \
                      xsum(self.y[flight.slot][j] for j in flight.airline.getOfferSlotRange(flight, 0)) == 0

        for flight in self.flights:
            for k in range(1,len(flight.airline.getOffersForFlight(flight))):
                self.m += self.x[flight.slot][k] + self.z[flight.slot][k] - \
                          xsum(self.y[flight.slot][j] for j in flight.airline.getOfferSlotRange(flight, k)) == 0

        for j in self.slot_indexes:
            self.m += xsum(self.y[i][j] for i in range(len(self.flights))) == 1

    def set_objective(self):

        self.m.objective = minimize(
            xsum(self.x[flight.slot, j] * self.score(flight, j) for flight in self.flights for j in self.slot_indexes) \
            + xsum(
                self.c[self.index(self.airlines, air)][self.index(air.flight_pairs, j)] for airline in self.airlines for j
                in
                air.flight_pairs))

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
        print("Simplex time ",end)

        print(self.m.status)

        self.solution_array = self.make_solution_array(self.x)

        self.solution = sol.Solution(self)

    def other_airlines_compatible_slots(self, flight):
        others_slots = self.df[self.df["airline"] != flight.airline.name]["slot"].to_numpy()
        return np.intersect1d(others_slots, flight.compatible_slots, assume_unique=True)

    def make_solution_array(self, x):
        solution_array = np.zeros((self.slot_indexes.shape[0], self.slot_indexes.shape[0]))
        for flight in self.flights:
            for j in self.slot_indexes:
                solution_array[flight.slot, j] = x[flight.slot, j].x
        return solution_array



