from typing import Callable

from Programma.ModelStructure import modelStructure as mS
from mip import *
import sys
from Programma.Istop.Solution import solution as sol
from itertools import combinations
from Programma.Istop import istopAirline as air
from Programma.Istop import istopFlight as modFl
from Programma.ModelStructure.Solution import solution
# from Programma.ModelStructure.Costs.costs import cost_function as cf

import numpy as np
import pandas as pd

import time


class Istop(mS.ModelStructure):

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

    def __init__(self, df_init, costFun: Union[Callable, List[Callable]], alpha=1, model_name="model"):

        self.preference_function = lambda x, y: x * (y ** alpha)
        # self.airlineConstructor = air.IstopAirline
        # self.flightConstructor = modFl.IstopFlight
        self.offers = None
        super().__init__(df_init=df_init, costFun=costFun, airline_ctor=air.IstopAirline)
        airline: air.IstopAirline
        for airline in self.airlines:
            airline.set_preferences(self.preference_function)

        self.airlines_pairs = np.array(list(combinations(self.airlines, 2)))

        self.epsilon = sys.float_info.min
        self.m = Model(model_name)
        self.x = None
        self.c = None
        self.m.threads = -1
        self.m.verbose = 0


        # self.initial_objective_value = sum([self.score(flight, flight.slot) for flight in self.flights])

    def set_variables(self):

        self.x = np.array([[self.m.add_var(var_type=BINARY) for j in self.slots] for i in self.slots])

        self.c = np.array(
            [[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])

        print("variabili", sum([len(var) for var in self.c]))

    def set_constraints(self):

        for eSlot in self.emptySlots:
            for slot in self.slots:
                self.m += self.x[eSlot.index, slot.index] == 0

        for flight in self.flights:
            self.m += xsum(self.x[flight.slot.index, slot.index] for slot in flight.compatibleSlots) == 1

        for j in self.slots:
            self.m += xsum(self.x[i.index, j.index] for i in self.slots) <= 1

        for flight in self.flights:
            for j in flight.notCompatibleSlots:
                self.m += self.x[flight.slot.index, j.index] == 0

        for flight in self.flights:

            self.m += xsum(self.x[flight.slot.index, slot_to_swap.index] for slot_to_swap in
                           self.other_airlines_compatible_slots(flight))\
                      <= xsum([self.c[flight.airline.index][j] for j in self.get_tuple(flight)])

        for flight in self.flights:
            for other_flight in flight.airline.flights:
                if flight != other_flight:
                    self.m += self.x[flight.slot.index, other_flight.slot.index] == 0

        k = 0
        for airl_pair in self.airlines_pairs:
            fl_pair_a = airl_pair[0].flight_pairs
            fl_pair_b = airl_pair[1].flight_pairs
            for pairA in fl_pair_a:
                for pairB in fl_pair_b:
                    self.condition(pairA, pairB)
                    self.m += xsum(self.x[i.slot.index, j.slot.index] for i in pairA for j in pairB) - \
                              xsum(self.x[i.slot.index, j.slot.index] for i in pairB for j in pairA) >= \
                              -(2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                                self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000

                    self.m += - xsum(self.x[i.slot.index, j.slot.index] for i in pairA for j in pairB) + \
                              xsum(self.x[i.slot.index, j.slot.index] for i in pairB for j in pairA) >= \
                              -(2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                                self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000

                    self.m += xsum(self.x[i.slot.index, j.slot.index] * i.costFun(i, j.slot) for i in pairA for j in pairB) - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 \
                              <= xsum(self.x[i.slot.index, j.slot.index] * i.costFun(i, i.slot) for i in pairA for j in pairB) - \
                              self.epsilon

                    self.m += xsum(self.x[i.slot.index, j.slot.index] * i.costFun(i, j.slot) for i in pairB for j in pairA) - \
                              (2 - self.c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                               self.c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 \
                              <= xsum(self.x[i.slot.index, j.slot.index] * i.costFun(i, i.slot) for i in pairB for j in pairA) - \
                              self.epsilon

                    k += 1
        print("vincoli", k)

    def set_objective(self):

        self.m.objective = minimize(
            xsum(self.x[flight.slot.index, j.index] * self.score(flight, j) for flight in self.flights for j in self.slots) \
            + xsum(
                self.c[self.index(self.airlines, air)][self.index(air.flight_pairs, j)] for air in self.airlines for j
                in
                air.flight_pairs))

    def run(self):

        self.set_variables()

        start = time.time()
        self.set_constraints()
        end = time.time() - start
        # print("Constraints setting time ", end)

        self.set_objective()

        # start = time.time()
        # self.m.optimize()
        # end = time.time() - start
        # print("Simplex time ", end)
        #
        # print(self.m.status)
        #
        # self.mipSolution = self.x
        #
        # solution.make_solution(self)
        #
        # self.offer_solution_maker()

    def other_airlines_compatible_slots(self, flight):
        others_slots = []
        for airline in self.airlines:
            if airline != flight.airline:
                others_slots.extend(airline.AUslots)
        otherAirlinesCompatibleSlots = []

        return np.intersect1d(others_slots, flight.compatibleSlots, assume_unique=True)

    def score(self, flight, slot):
        return (flight.preference * flight.delay(slot) ** 2) / 2

    def offer_solution_maker(self):

        flight: modFl.IstopFlight
        airline_names = ["total"] + [airline.name for airline in self.airlines]
        offers = [sum([1 for flight in self.flights if flight.slot != flight.newSlot]) / 2]
        for airline in self.airlines:
            offers.append(sum([1 for flight in airline.flights if flight.slot != flight.newSlot]) / 2)

        offers = np.array(offers).astype(int)
        self.offers = pd.DataFrame({"airline": airline_names, "offers": offers})

    def condition(self, pairA, pairB):

        A0 = pairA[0]
        A1 = pairA[1]
        B0 = pairB[0]
        B1 = pairB[1]

        initial_costA = A0.costFun(A0, A0.slot) + A1.costFun(A1, A1.slot)
        initial_costB = B0.costFun(B0, B0.slot) + B1.costFun(B1, B1.slot)

        offA1 = initial_costA - A0.costFun(A0, B0.slot) - A1.costFun(A1, B1.slot)
        offA2 = initial_costA - A0.costFun(A0, B1.slot) - A1.costFun(A1, B0.slot)
        offB1 = initial_costB - B0.costFun(B0, A0.slot) - B1.costFun(B1, A1.slot)
        offB2 = initial_costB - B0.costFun(B0, A1.slot) - B1.costFun(B1, A0.slot)

        if offA1 > 0 and offB1 > 0 and A0.etaSlot <= B0.slot and B0.etaSlot <= A0.slot and \
                A1.etaSlot <= B1.slot and B1.etaSlot <= A1.slot:
            print(A0, A0.slot, "<->", B0.slot, B0)
            print(A1, A1.slot, "<->", B1.slot, B1)
            print(A0, A0.delay(A0.slot), A0.delay(B0.slot))
            print(B0, B0.delay(B0.slot), B0.delay(A0.slot))
            print(A1, A1.delay(A1.slot), A1.delay(B1.slot))
            print(B1, B1.delay(B1.slot), B1.delay(A1.slot))
            print(offA1, offB1, "\n")

        if offA2 > 0 and offB2 > 0 and A0.etaSlot <= B1.slot and B1.etaSlot <= A0.slot and \
                A1.etaSlot <= B0.slot and B0.etaSlot <= A1.slot:
            print(A0, A0.slot, "<->", B1.slot, B1)
            print(A1, A1.slot, "<->", B0.slot, B0)
            print(A0, A0.delay(A0.slot), A0.delay(B1.slot))
            print(B0, B0.delay(B0.slot), B0.delay(A1.slot))
            print(A1, A1.delay(A1.slot), A1.delay(B0.slot))
            print(B1, B1.delay(B1.slot), B1.delay(A0.slot))
            print(offA2, offB2, "\n")

        if offA1 > 0 and offB2 > 0 and A0.etaSlot <= B0.slot and B0.etaSlot <= A1.slot and \
                A1.etaSlot <= B1.slot and B1.etaSlot <= A0.slot:
            print(A0, A0.slot, "->", B0.slot, B0, "->", A1, A1.slot, "->", B1.slot, B1)
            print(A0, A0.delay(A0.slot), A0.delay(B0.slot))
            print(B0, B0.delay(B0.slot), B0.delay(A1.slot))
            print(A1, A1.delay(A1.slot), A1.delay(B1.slot))
            print(B1, B1.delay(B1.slot), B1.delay(A0.slot))
            print(offA1, offB2, "\n")

        if offA2 > 0 and offB1 > 0 and A0.etaSlot <= B1.slot and B1.etaSlot <= A0.slot and \
                A1.etaSlot <= B0.slot and B0.etaSlot <= A1.slot:
            print(A0, A0.slot, "<->", B1.slot, B1, "->", A1, A1.slot, "->", B0.slot, B0)
            print(A0, A0.delay(A0.slot), A0.delay(B1.slot))
            print(B0, B0.delay(B0.slot), B0.delay(A0.slot))
            print(A1, A1.delay(A1.slot), A1.delay(B0.slot))
            print(B1, B1.delay(B1.slot), B1.delay(A1.slot))
            print(offA2, offB1, "\n")
