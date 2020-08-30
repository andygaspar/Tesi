from Programma.ModelStructure import modelStructure as mS
from mip import *
import sys
from Programma.Mip.Solution import solution as sol
from itertools import combinations
from Programma.Mip import modelAirline as air
from Programma.Mip import modelFlight as modFl
from Programma.ModelStructure.Solution import solution
from Programma.ModelStructure.Costs.costs import cost_function as cf

import numpy as np
import pandas as pd

import time


class MipModel(mS.ModelStructure):

    @staticmethod
    def index(array, elem):
        for i in range(len(array)):
            if np.array_equiv(array[i], elem):
                return i

    def get_couple(self, couple):
        index = 0
        for c in self.couples:
            if couple[0].num == c[0].num and couple[1].num == c[1].num:
                return index
            index += 1

    def get_match_for_flight(self, flight):
        j = 0
        indexes = []
        for match in self.matches:
            for couple in match:
                if flight.num == couple[0].num or flight.num == couple[1].num:
                    indexes.append(j)
            j += 1
        return indexes

    def __init__(self, df_init, alpha=1, cost_kind="quadratic", model_name="model"):

        self.f = lambda x, y: x * (y ** alpha)
        self.airlineConstructor = air.ModelAirline
        self.flightConstructor = modFl.ModelFlight
        self.offers = None
        super().__init__(df_init=df_init, cost_kind=cost_kind)

        self.airlines_pairs = np.array(list(combinations(self.airlines, 2)))

        self.epsilon = sys.float_info.min
        self.m = Model(model_name)
        self.x = None
        self.c = None
        self.m.threads = -1
        self.m.verbose = 0

        self.matches = []
        self.couples = []
        self.flights_in_matches = []

        self.initial_objective_value = sum([self.score(flight, flight.slot) for flight in self.flights])

    def set_variables(self):

        for airl_pair in self.airlines_pairs:
            fl_pair_a = airl_pair[0].flight_pairs
            fl_pair_b = airl_pair[1].flight_pairs
            for pairA in fl_pair_a:
                for pairB in fl_pair_b:
                    if self.condition(pairA, pairB):
                        self.matches.append([pairA, pairB])

        for match in self.matches:
            for couple in match:
                if not self.is_in(couple, self.couples):
                    self.couples.append(couple)
                    if not self.f_in_matched(couple[0]):
                        self.flights_in_matches.append(couple[0])
                    if not self.f_in_matched(couple[1]):
                        self.flights_in_matches.append(couple[1])
        self.x = np.array([[self.m.add_var(var_type=BINARY) for j in self.slotIndexes] for i in self.slotIndexes])

        self.c = np.array([self.m.add_var(var_type=BINARY) for i in self.matches])
        print("preprocess concluded.  number of couples: *******  ", len(self.c))

    def set_constraints(self):

        for i in self.empty_slots:
            for j in self.slotIndexes:
                self.m += self.x[i, j] == 0

        for flight in self.flights:
            self.m += xsum(self.x[flight.slot, j] for j in flight.compatible_slots) == 1
            if not self.f_in_matched(flight):
                self.m += self.x[flight.slot, flight.slot] == 1

        for j in self.slotIndexes:
            self.m += xsum(self.x[i, j] for i in self.slotIndexes) <= 1

        for flight in self.flights:
            for j in flight.not_compatible_slots:
                self.m += self.x[flight.slot, j] == 0

        for flight in self.flights_in_matches:
            self.m += xsum(self.x[flight.slot, slot_to_swap] for slot_to_swap in
                           [s for s in self.slotIndexes if s != flight.slot]) \
                      == xsum([self.c[j] for j in self.get_match_for_flight(flight)])

        for flight in self.flights:
            for other_flight in flight.airline.flights:
                if flight != other_flight:
                    self.m += self.x[flight.slot, other_flight.slot] == 0

        k = 0
        for match in self.matches:
            pairA = match[0]
            pairB = match[1]

            self.m += xsum(self.x[i.slot, j.slot] for i in pairA for j in pairB) + \
                      xsum(self.x[i.slot, j.slot] for i in pairB for j in pairA) >= \
                      (self.c[k]) * 4


            self.m += xsum(self.x[i.slot, j.slot] * cf(self, i, j.slot) for i in pairA for j in pairB) - \
                      (1-self.c[k]) * 100000 \
                      <= xsum(self.x[i.slot, j.slot] * cf(self, i, i.slot) for i in pairA for j in pairB) - \
                      self.epsilon

            self.m += xsum(self.x[i.slot, j.slot] * cf(self, i, j.slot) for i in pairB for j in pairA) - \
                      (1-self.c[k]) * 100000 \
                      <= xsum(self.x[i.slot, j.slot] * cf(self, i, i.slot) for i in pairB for j in pairA) - \
                      self.epsilon

            k += 1

    def set_objective(self):

        self.m.objective = minimize(
            xsum(self.x[flight.slot, j] * self.score(flight, j) for flight in self.flights for j in self.slotIndexes))

    def run(self):

        self.set_variables()

        start = time.time()
        self.set_constraints()
        end = time.time() - start
        # print("Constraints setting time ", end)

        self.set_objective()

        start = time.time()
        self.m.optimize()
        end = time.time() - start
        # print("Simplex time ", end)

        print(self.m.status)
        print(len(self.matches))
        self.mipSolution = self.x

        solution.make_solution(self)

        self.offer_solution_maker()


        # for i in self.slotIndexes:
        #     if self.x[i, i].x == 0:
        #         for j in self.slotIndexes:
        #             if self.x[i, j].x != 0:
        #                 print(i, j)

        for i in self.slotIndexes:
            if self.flights[i].eta_slot > self.flights[i].slot:
                print("********************** danno *********************************")


        # for i in range(len(self.matches)):
        #     if self.c[i].x != 0:
        #         print(self.matches[i])

    def other_airlines_compatible_slots(self, flight):
        others_slots = self.df[self.df["airline"] != flight.airline.name]["slot"].to_numpy()
        return np.intersect1d(others_slots, flight.compatible_slots, assume_unique=True)

    def score(self, flight, j):
        return (flight.preference * self.delays[flight.slot, j] ** 2) / 2

    def offer_solution_maker(self):

        flight: modFl.ModelFlight
        airline_names = ["total"] + [airline.name for airline in self.airlines]
        flights_numbers = [self.num_flights] + [len(airline.flights) for airline in self.airlines]
        offers = [sum([1 for flight in self.flights if flight.slot != flight.new_slot]) / 4]
        for airline in self.airlines:
            offers.append(sum([1 for flight in airline.flights if flight.slot != flight.new_slot]) / 2)

        offers = np.array(offers).astype(int)
        self.offers = pd.DataFrame({"airline": airline_names, "flights": flights_numbers, "offers": offers})
        self.offers.sort_values(by="flights", inplace=True, ascending=False)

    def condition(self, pairA, pairB):

        A0 = pairA[0]
        A1 = pairA[1]
        B0 = pairB[0]
        B1 = pairB[1]

        initial_costA = cf(self, A0, A0.slot) + cf(self, A1, A1.slot)
        initial_costB = cf(self, B0, B0.slot) + cf(self, B1, B1.slot)

        offA1 = initial_costA - cf(self, A0, B0.slot) - cf(self, A1, B1.slot)
        offA2 = initial_costA - cf(self, A0, B1.slot) - cf(self, A1, B0.slot)
        offB1 = initial_costB - cf(self, B0, A0.slot) - cf(self, B1, A1.slot)
        offB2 = initial_costB - cf(self, B0, A1.slot) - cf(self, B1, A0.slot)

        if offA1 > 0 and offB1 > 0 and A0.eta_slot <= B0.slot and B0.eta_slot <= A0.slot and \
                A1.eta_slot <= B1.slot and B1.eta_slot <= A1.slot:
            # print(A0, A0.slot, "<->", B0.slot, B0)
            # print(A1, A1.slot, "<->", B1.slot, B1)
            # print(A0, self.delays[A0.num, A0.slot], self.delays[A0.num, B0.slot])
            # print(B0, self.delays[B0.num, B0.slot], self.delays[B0.num, A0.slot])
            # print(A1, self.delays[A1.num, A1.slot], self.delays[A1.num, B1.slot])
            # print(B1, self.delays[B1.num, B1.slot], self.delays[B1.num, A1.slot])
            # print(offA1, offB1, "\n")
            return True

        if offA2 > 0 and offB2 > 0 and A0.eta_slot <= B1.slot and B1.eta_slot <= A0.slot and \
                A1.eta_slot <= B0.slot and B0.eta_slot <= A1.slot:
            # print(A0, A0.slot, "<->", B1.slot, B1)
            # print(A1, A1.slot, "<->", B0.slot, B0)
            # print(A0, self.delays[A0.num, A0.slot], self.delays[A0.num, B1.slot])
            # print(B0, self.delays[B0.num, B0.slot], self.delays[B0.num, A1.slot])
            # print(A1, self.delays[A1.num, A1.slot], self.delays[A1.num, B0.slot])
            # print(B1, self.delays[B1.num, B1.slot], self.delays[B1.num, A0.slot])
            # print(offA2, offB2, "\n")
            return True

        if offA1 > 0 and offB2 > 0 and A0.eta_slot <= B0.slot and B0.eta_slot <= A1.slot and \
                A1.eta_slot <= B1.slot and B1.eta_slot <= A0.slot:
            # print(A0, A0.slot, "->", B0.slot, B0, "->", A1, A1.slot, "->", B1.slot, B1)
            # print(A0, self.delays[A0.num, A0.slot], self.delays[A0.num, B0.slot])
            # print(B0, self.delays[B0.num, B0.slot], self.delays[B0.num, A1.slot])
            # print(A1, self.delays[A1.num, A1.slot], self.delays[A1.num, B1.slot])
            # print(B1, self.delays[B1.num, B1.slot], self.delays[B1.num, A0.slot])
            # print(offA1, offB2, "\n")
            return True

        if offA2 > 0 and offB1 > 0 and A0.eta_slot <= B1.slot and B1.eta_slot <= A0.slot and \
                A1.eta_slot <= B0.slot and B0.eta_slot <= A1.slot:
            # print(A0, A0.slot, "<->", B1.slot, B1, "->", A1, A1.slot, "->", B0.slot, B0)
            # print(A0, self.delays[A0.num, A0.slot], self.delays[A0.num, B1.slot])
            # print(B0, self.delays[B0.num, B0.slot], self.delays[B0.num, A0.slot])
            # print(A1, self.delays[A1.num, A1.slot], self.delays[A1.num, B0.slot])
            # print(B1, self.delays[B1.num, B1.slot], self.delays[B1.num, A1.slot])
            # print(offA2, offB1, "\n")
            return True

        return False

    @staticmethod
    def is_in(couple, couples):
        for c in couples:
            if couple[0].num == c[0].num and couple[1].num == c[1].num:
                return True
            if couple[1].num == c[0].num and couple[0].num == c[1].num:
                return True
            return False

    def f_in_matched(self, flight):
        for f in self.flights_in_matches:
            if f.num == flight.num:
                return True
        return False
