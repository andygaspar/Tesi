import flight as fl
import airline as al
import modelStructure as mS
from mip import *

import numpy as np
import pandas as pd
from itertools import combinations, product


class MipModel(mS.ModelStructure):

    @staticmethod
    def index(array, elem):
        for i in range(len(array)):
            if np.array_equiv(array[i], elem):
                return i

    def get_tuple(self, flight):
        j = 0
        indexes = []
        for pair in self.which_airline(flight).flight_pairs:
            if flight in pair:
                indexes.append(j)
            j += 1
        return indexes

    def __init__(self, df_in, f=lambda x, y: x * y, model_name="model"):
        super().__init__(df_in, f, model_name)
        self.airlines_pairs = al.Airline.pairs(self.airlines)

        self.m = Model(model_name)
        self.m.verbose = 0

        self.solutionX = None
        self.solutionC = None

    # noinspection SpellCheckingInspection
    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for j in self.slots] for i in self.slots])

        c = np.array([[self.m.add_var(var_type=BINARY) for i in airl.flight_pairs] for airl in self.airlines])

        for i in self.empty_slots:
            for j in self.slots:
                print(j, type(j))
                self.m += x[i, j] == 0

        for flight in self.flights:
            self.m += xsum(x[flight.slot, j] for j in flight.compatible_slots) == 1

        for j in self.slots:
            self.m += xsum(x[i, j] for i in self.slots) <= 1

        for flight in self.flights:
            for j in flight.not_compatible_slots:
                self.m += x[flight.slot, j] == 0

        for flight in self.flights:
            for slot_to_swap in self.other_airlines_slot(flight):
                self.m += x[flight.slot, slot_to_swap] <= xsum(
                    [c[self.which_airline(flight).airline_index][j] for j in self.get_tuple(flight)])

        for airl_pair in self.airlines_pairs:
            fl_pair_a = airl_pair[0].flight_pairs
            fl_pair_b = airl_pair[1].flight_pairs
            for pairA in fl_pair_a:
                for pairB in fl_pair_b:
                    print(pairA)
                    print(pairB, "\n")
                    self.m += xsum(x[i.slot, j.slot] for i in pairA for j in pairB) + \
                              xsum(x[i.slot, j.slot] for i in pairB for j in pairA) \
                              >= (c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)]
                                  + c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 2 \
                              - (2 - c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                                 c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000

                    self.m += xsum(x[i.slot, j.slot] * self.score(i, j.slot) for i in pairA for j in pairB) \
                              - (2 - c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                                 c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 100000 <= \
                              xsum(x[i.slot, j.slot] * self.score(i, i.slot) for i in pairA for j in pairB) - self.e

                    self.m += xsum(x[i.slot, j.slot] * self.score(i, j.slot) for i in pairB for j in pairA) \
                              - (2 - c[self.index(self.airlines, airl_pair[0])][self.index(fl_pair_a, pairA)] -
                                 c[self.index(self.airlines, airl_pair[1])][self.index(fl_pair_b, pairB)]) * 10000 <= \
                              xsum(x[i.slot, j.slot] * self.score(i, i.slot) for i in pairB for j in pairA) - self.e

        self.m.objective = minimize(
            xsum(x[flight.slot, j] * self.score(flight, j) for flight in self.flights for j in self.slots) \
            + xsum(c[self.index(self.airlines, air)][self.index(air.flight_pairs, j)] for air in self.airlines for j in
                   air.flight_pairs))

        self.m.optimize()
        self.solutionX = x
        self.solutionC = c

        for j in self.slots:
            for i in self.slots:
                if x[i, j].x != 0:
                    print(self.df.iloc[i]["flight"],self.df.iloc[i]["airline"],self.df.iloc[i]["eta"],self.schedule[j],
                          self.df.iloc[i]["costs"]*self.delays[i,j])
                    self.solution_schedule.append((i, j))
        #
        # for air in self.airlines:
        #     for flight_pair in air.flight_pairs:
        #         if c[self.index(self.airlines, air)][self.index(air.flight_pairs, flight_pair)].x != 0:
        #             self.offers.append((air, flight_pair))

    @staticmethod
    def other_airlines_slot(flight):
        return df[df["airline"] != flight.airline.name]["slot"].to_numpy()


# df = pd.read_csv("data/ruiz.csv")
# df["costs"] = np.zeros(df.shape[0])
df = pd.read_csv("data/sample.csv")
model = MipModel(df)
model.run()

model.print_solution()
# print(df)
#

# fli = model.flights[51]
# print(fli.slot, fli, fli.compatible_slots)
