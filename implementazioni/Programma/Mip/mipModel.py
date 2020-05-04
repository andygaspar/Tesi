from Programma.ModelStructure import modelStructure as mS
from mip import *
import sys
from Programma.Mip.Solution import solution as sol
from itertools import combinations
from Programma.Mip import modelAirline as air
from Programma.Mip import modelFlight as modFl
from Programma.ModelStructure.Solution import solution

import numpy as np

import time


class MipModel(mS.ModelStructure):

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

    def __init__(self, df_init, f=lambda x, y: x * y, cost_kind="quadratic", model_name="model"):

        self.f = f
        self.airlineConstructor = air.ModelAirline
        self.flightConstructor = modFl.ModelFlight
        super().__init__(df_init=df_init, cost_kind=cost_kind)

        self.airlines_pairs = np.array(list(combinations(self.airlines, 2)))

        self.epsilon = sys.float_info.min
        self.m = Model(model_name)
        self.x = None
        self.c = None
        self.m.threads = -1
        self.m.verbose = 0

        self.initial_objective_value = sum([self.score(flight, flight.slot) for flight in self.flights])

    def set_variables(self):

        self.x = np.array([[self.m.add_var(var_type=BINARY) for j in self.slotIndexes] for i in self.slotIndexes])

        self.c = np.array(
            [[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])

    def set_constraints(self):

        for i in self.empty_slots:
            for j in self.slotIndexes:
                self.m += self.x[i, j] == 0

        for flight in self.flights:
            self.m += xsum(self.x[flight.slot, j] for j in flight.compatible_slots) == 1

        for j in self.slotIndexes:
            self.m += xsum(self.x[i, j] for i in self.slotIndexes) <= 1

        for flight in self.flights:
            for j in flight.not_compatible_slots:
                self.m += self.x[flight.slot, j] == 0

        for flight in self.flights:
            for slot_to_swap in self.other_airlines_compatible_slots(flight):
                self.m += self.x[flight.slot, slot_to_swap] <= xsum(
                    [self.c[flight.airline.index][j] for j in self.get_tuple(flight)])

        for flight in self.flights:
            for other_flight in flight.airline.flights:
                if flight != other_flight:
                    self.m += self.x[flight.slot, other_flight.slot] == 0

        for airl_pair in self.airlines_pairs:
            fl_pair_a = airl_pair[0].flight_pairs
            fl_pair_b = airl_pair[1].flight_pairs
            for pairA in fl_pair_a:
                for pairB in fl_pair_b:
                    self.m += xsum(self.x[i.slot, j.slot] for i in pairA for j in pairB) + \
                              xsum(self.x[i.slot, j.slot] for i in pairB for j in pairA) >= \
                              (self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] +
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 2 - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000

                    self.m += xsum(self.x[i.slot, j.slot] * self.score(i, j.slot) for i in pairA for j in pairB) - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 \
                              <= xsum(self.x[i.slot, j.slot] * self.score(i, i.slot) for i in pairA for j in pairB) - \
                              self.epsilon

                    self.m += xsum(self.x[i.slot, j.slot] * self.score(i, j.slot) for i in pairB for j in pairA) - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 \
                              <= xsum(self.x[i.slot, j.slot] * self.score(i, i.slot) for i in pairB for j in pairA) - \
                              self.epsilon

    def set_objective(self):

        self.m.objective = minimize(
            xsum(self.x[flight.slot, j] * self.score(flight, j) for flight in self.flights for j in self.slotIndexes) \
            + xsum(
                self.c[self.index(self.airlines, air)][self.index(air.flight_pairs, j)] for air in self.airlines for j
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
        print("Simplex time ", end)

        print(self.m.status)

        self.mipSolution = self.x
        # solution.make_solution_array(self)
        # self.solution = sol.Solution(self)
        solution.make_solution(self)

    def other_airlines_compatible_slots(self, flight):
        others_slots = self.df[self.df["airline"] != flight.airline.name]["slot"].to_numpy()
        return np.intersect1d(others_slots, flight.compatible_slots, assume_unique=True)

    def score(self, flight, j):
        return (flight.preference * self.delays[flight.slot, j] ** 2) / 2
