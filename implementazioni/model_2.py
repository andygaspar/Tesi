import numpy as np

from model import *


def ind(array, elem):
    for i in range(len(array)):
        if np.array_equiv(array[i], elem):
            return i


class model_2(model):

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
        self.offers = []
        self.temp = None

    def run(self):

        x = np.array([[self.m.add_var(var_type=BINARY) for i in self.slots] for j in self.slots])

        c = np.array([[self.m.add_var(var_type=BINARY) for i in airline.flight_pairs] for airline in self.airlines])

        for i in range(len(self.slots)):
            self.m += xsum(x[i, j] for j in np.append(np.setdiff1d(self.slots, self.which_airline(i).flights), i)) == 1

        for j in range(len(self.slots)):
            self.m += xsum(x[i, j] for i in self.slots) <= 1

        for i, j in product(self.slots, self.slots):
            if j < self.ETA_index[i]:
                self.m += x[i, j] == 0

        for i in self.slots:
            for j in np.setdiff1d(self.slots, self.which_airline(i).flights):
                self.m += x[i, j] <= xsum([c[ind(self.airlines, self.which_airline(i))][j] for j in self.get_tuple(i)])

        for air_pair in self.airlines_pairs:
            airlineA = air_pair[0].flight_pairs
            airlineB = air_pair[1].flight_pairs
            for pairA in airlineA:
                for pairB in airlineB:
                    self.m += xsum(x[i, j] for i in pairA for j in pairB) + xsum(x[i, j] for i in pairB for j in pairA) \
                              >= (c[ind(self.airlines, air_pair[0])][ind(airlineA, pairA)]
                                  + c[ind(self.airlines, air_pair[1])][ind(airlineB, pairB)]) * 2 \
                              - (2 - c[ind(self.airlines, air_pair[0])][ind(airlineA, pairA)] -
                                 c[ind(self.airlines, air_pair[1])][ind(airlineB, pairB)]) * 100000

                    self.m += xsum(x[i, j] * self.score(air_pair[0], i, j) for i in pairA for j in pairB) \
                              - (2 - c[ind(self.airlines, air_pair[0])][ind(airlineA, pairA)] -
                                 c[ind(self.airlines, air_pair[1])][ind(airlineB, pairB)]) * 100000 <= \
                              xsum(x[i, j] * self.score(air_pair[0], i, i) for i in pairA for j in pairB) - self.e

                    self.m += xsum(x[i, j] * self.score(air_pair[1], i, j) for i in pairB for j in pairA) \
                              - (2 - c[ind(self.airlines, air_pair[0])][ind(airlineA, pairA)] -
                                 c[ind(self.airlines, air_pair[1])][ind(airlineB, pairB)]) * 10000 <= \
                              xsum(x[i, j] * self.score(air_pair[1], i, i) for i in pairB for j in pairA) - self.e

        self.m.objective = minimize(
            xsum(x[i, j] * self.score(a, i, j) for a in self.airlines for i in a.flights for j in self.slots) \
            + xsum(c[ind(self.airlines, airline)][ind(airline.flight_pairs, j)] for airline in self.airlines for j in
                   airline.flight_pairs))

        self.m.optimize()
        self.solution = x

        for j in self.slots:
            for i in self.slots:
                if x[i, j].x != 0:
                    self.new_schedule.append((i, j))

        for airline in self.airlines:
            for flight_pair in airline.flight_pairs:
                if c[ind(self.airlines, airline)][ind(airline.flight_pairs, flight_pair)].x != 0:
                    self.offers.append((airline, flight_pair))

        self.temp = c

    def find_match(self, i):
        for j in self.solts[self.slots != i]:
            if self.solution[i, j].x == 1:
                return j

    #
    # def print_costs:
    #     for airline in self.airlines:
    #         costs=0
    #         for

    def print_offers(self):
        offers_found = []
        flights_selected = []
        for airline in self.airlines:
            for flight_pair in airline.flight_pairs:
                if (airline, flight_pair) in self.offers:
                    print("(", airline, ",", self.which_airline(self.find_match(flight_pair[0])), ")")
                    for flight in flight_pair:
                        print(self.get_flights_name(flight), " -> ", self.get_flights_name(self.find_match(flight)))


# BA=airline("BA",[1,4,5],[4,9,12])
# YA=airline("YA",[0,2,3,6],[1,14,1,15])
# ETA=np.array(range(7))
# FPFS=ETA*2

BA = airline("BA", [1, 4, 5], [1, 20, 1])
YA = airline("YA", [0, 2, 3, 6], [1, 14, 1, 1])
ETA = np.array(range(7))
FPFS = ETA * 8

problem = model_2([BA, YA], ETA, FPFS)
problem.run()

problem.print_schedule()
problem.print_solution()

for l in problem.temp:
    row = []
    for c in l:
        row.append(c.x)
    print(row)

for i in problem.slots:
    row = []
    for j in problem.slots:
        row.append(problem.solution[i, j].x)
    print(row)


BA = airline("BA", [1, 4, 5], [4, 9, 12])
YA = airline("YA", [0, 2, 3, 6], [1, 14, 1, 15])
ETA = np.array(range(7))
FPFS = ETA * 2

problem = model_2([BA, YA], ETA, FPFS)
problem.run()

problem.print_schedule()
problem.print_solution()

for l in problem.temp:
    row = []
    for c in l:
        row.append(c.x)
    print(row)
