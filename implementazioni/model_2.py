import numpy as np

from modelStructure import *





class model_2(modelStructure):

    def index(self,array, elem):
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

    def __init__(self, airlines, ETA, FPFS_scheduling, f=lambda x: x):
        super().__init__(airlines, ETA, FPFS_scheduling, f=lambda x: x)
        self.airlines_pairs = pairs(self.airlines)

    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

        c = np.array([[self.m.add_var(var_type=BINARY) for i in air.flight_pairs] for air in self.airlines])

        for i in range(len(self.slots)):
            self.m += xsum(x[i, j] for j in np.append(np.setdiff1d(self.slots, self.which_airline(i).flights), i)) == 1

        for j in range(len(self.slots)):
            self.m += xsum(x[i, j] for i in self.slots) <= 1

        for i, j in product(self.slots, self.slots):
            if j < self.ETA_index[i]:
                self.m += x[i, j] == 0

        for i in self.slots:
            for j in np.setdiff1d(self.slots, self.which_airline(i).flights):
                self.m += x[i, j] <= xsum([c[self.index(self.airlines, self.which_airline(i))][j] for j in self.get_tuple(i)])

        for air_pair in self.airlines_pairs:
            airApairs = air_pair[0].flight_pairs
            airBpairs = air_pair[1].flight_pairs
            for pairA in airApairs:
                for pairB in airBpairs:
                    self.m += xsum(x[i, j] for i in pairA for j in pairB) + xsum(x[i, j] for i in pairB for j in pairA) \
                              >= (c[self.index(self.airlines, air_pair[0])][self.index(airApairs, pairA)]
                                  + c[self.index(self.airlines, air_pair[1])][self.index(airBpairs, pairB)]) * 2 \
                              - (2 - c[self.index(self.airlines, air_pair[0])][self.index(airApairs, pairA)] -
                                 c[self.index(self.airlines, air_pair[1])][self.index(airBpairs, pairB)]) * 100000

                    self.m += xsum(x[i, j] * self.score(air_pair[0], i, j) for i in pairA for j in pairB) \
                              - (2 - c[self.index(self.airlines, air_pair[0])][self.index(airApairs, pairA)] -
                                 c[self.index(self.airlines, air_pair[1])][self.index(airBpairs, pairB)]) * 100000 <= \
                              xsum(x[i, j] * self.score(air_pair[0], i, i) for i in pairA for j in pairB) - self.e

                    self.m += xsum(x[i, j] * self.score(air_pair[1], i, j) for i in pairB for j in pairA) \
                              - (2 - c[self.index(self.airlines, air_pair[0])][self.index(airApairs, pairA)] -
                                 c[self.index(self.airlines, air_pair[1])][self.index(airBpairs, pairB)]) * 10000 <= \
                              xsum(x[i, j] * self.score(air_pair[1], i, i) for i in pairB for j in pairA) - self.e

        self.m.objective = minimize(
            xsum(x[i, j] * self.score(a, i, j) for a in self.airlines for i in a.flights for j in self.slots) \
            + xsum(c[self.index(self.airlines, air)][self.index(air.flight_pairs, j)] for air in self.airlines for j in
                   air.flight_pairs))

        self.m.optimize()
        self.solutionX = x
        self.solutionC = c

        for j in self.slots:
            for i in self.slots:
                if x[i, j].x != 0:
                    self.new_schedule.append((i, j))

        for air in self.airlines:
            for flight_pair in air.flight_pairs:
                if c[self.index(self.airlines, air)][self.index(air.flight_pairs, flight_pair)].x != 0:
                    self.offers.append((air, flight_pair))
