from Programma.ModelStructure.Airline import airline as al
from Programma.ModelStructure import modelStructure as mS
import xpress as xp
from Programma.Istop.Solution import solution as sol

import numpy as np

import time


class XpressModel(mS.ModelStructure):

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

    def __init__(self, df_in, f=lambda x, y: x * y, model_name="model"):

        super().__init__(df_in, f, model_name)

        self.airlines_pairs = al.Airline.pairs(self.airlines)

        self.m = xp.problem()
        self.x = None
        self.c = None

    def set_variables(self):

        self.x = np.array([[xp.var(vartype=xp.binary) for j in self.slotIndexes] for i in self.slotIndexes])

        self.c = np.array([[xp.var(vartype=xp.binary) for i in airl.flight_pairs] for airl in self.airlines])

        self.m.addVariable(self.x, self.c)

    def set_constraints(self):

        for i in self.emptySlots:
            for j in self.slotIndexes:
                self.m.addConstraint(self.x[i, j] == 0)

        for flight in self.flights:
            self.m.addConstraint(xp.Sum(self.x[flight.slot, j] for j in flight.compatible_slots) == 1)

        for j in self.slotIndexes:
            self.m.addConstraint(xp.Sum(self.x[i, j] for i in self.slotIndexes) <= 1)

        for flight in self.flights:
            for j in flight.not_compatible_slots:
                self.m.addConstraint(self.x[flight.slot, j] == 0)

        for flight in self.flights:
            for slot_to_swap in self.other_airlines_compatible_slots(flight):
                self.m.addConstraint(self.x[flight.slot, slot_to_swap] <= xp.Sum(
                    [self.c[flight.airline.index][j] for j in self.get_tuple(flight)]))

        for flight in self.flights:
            for other_flight in flight.airline.flights:
                if flight != other_flight:
                    self.m.addConstraint(self.x[flight.slot, other_flight.slot] == 0)

        for airl_pair in self.airlines_pairs:
            fl_pair_a = airl_pair[0].flight_pairs
            fl_pair_b = airl_pair[1].flight_pairs
            for pairA in fl_pair_a:
                for pairB in fl_pair_b:
                    self.m.addConstraint(xp.Sum(self.x[i.slot, j.slot] for i in pairA for j in pairB) + \
                              xp.Sum([self.x[i.slot, j.slot] for i in pairB for j in pairA]) >= \
                              (self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] +
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 2 - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000)

                    self.m.addConstraint(xp.Sum(self.x[i.slot, j.slot] * self.score(i, j.slot) for i in pairA for j in pairB) - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 \
                              <= xp.Sum(self.x[i.slot, j.slot] * self.score(i, i.slot) for i in pairA for j in pairB) - \
                              self.epsilon)

                    self.m.addConstraint(xp.Sum(self.x[i.slot, j.slot] * self.score(i, j.slot) for i in pairB for j in pairA) - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 \
                              <= xp.Sum(self.x[i.slot, j.slot] * self.score(i, i.slot) for i in pairB for j in pairA) - \
                              self.epsilon)

    def set_objective(self):

        self.m.setObjective(
            xp.Sum(self.x[flight.slot, j] * self.score(flight, j) for flight in self.flights for j in self.slotIndexes) \
            + xp.Sum(
                self.c[self.index(self.airlines, air)][self.index(air.flight_pairs, j)] for air in self.airlines for j
                in
                air.flight_pairs), sense=xp.minimize)

    def run(self):

        self.set_variables()

        start = time.time()
        self.set_constraints()
        end = time.time() - start
        print("Constraints setting time ", end)

        self.set_objective()

        start = time.time()
        self.m.solve()
        end = time.time() - start
        print("Simplex time ",end)

        print(self.m.status)

        self.solution_array = self.make_solution_array(self.x)

        self.solution = sol.Solution(self)

    def other_airlines_compatible_slots(self, flight):
        others_slots = self.df[self.df["airline"] != flight.airline.name]["slot"].to_numpy()
        return np.intersect1d(others_slots, flight.compatible_slots, assume_unique=True)

    def make_solution_array(self, x):
        solution_array = np.zeros((self.slotIndexes.shape[0], self.slotIndexes.shape[0]))
        for flight in self.flights:
            for j in self.slotIndexes:
                solution_array[flight.slot, j] = x[flight.slot, j].x
        return solution_array



