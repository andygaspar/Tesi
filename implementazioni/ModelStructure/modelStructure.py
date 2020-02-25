from Airline import airline as air
from ModelStructure import flightList as fll
from ModelStructure import airlineList as airll

import numpy as np
import pandas as pd
from itertools import product
import sys


class ModelStructure:

    def compute_delays(self):
        delays = np.zeros((self.slot_indexes.shape[0], self.slot_indexes.shape[0]))
        for flight, j in product(self.flights, self.slot_indexes):
            delays[flight.slot, j] = abs(self.gdp_schedule[j] - flight.slot)
        return delays

    def __init__(self, int_df, f, model_name):

        self.epsilon = sys.float_info.min

        self.df = int_df

        self.f = f

        self.slot_indexes = np.array(self.df["slot"])

        self.gdp_schedule = self.df["gdp schedule"]

        self.airlines = airll.make_airlines_list(self)

        self.num_airlines = len(np.unique(self.df["airline"]))

        self.flights = fll.make_flight_list(self)

        self.num_flights = len(self.flights)

        self.delays = self.compute_delays()

        self.empty_slots = self.df[int_df["flight"] == "Empty"]["slot"].to_numpy()

        # self.slot_to_flight = dict(zip(self.int_df[self.int_df["flight"] != "Empty"]["slot"], range(len(self.flights))))

        # self.solution_df = None

        # self.solutionX = None

        # self.offers = []

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def score(self, flight, j):
        return self.delays[flight.slot, j] * flight.preference

    def which_airline(self, flight):
        for a in self.airlines:
            if flight in a.flights:
                return a

    def get_flights_name(self, i):
        return self.which_airline(i).flights_name[i]

    def print_schedule(self):
        print(self.df)

    def print_solution(self):
        print(self.solution_df)

    def find_match(self, i):
        for j in self.slot_indexes[self.slot_indexes != i]:
            if self.solutionX[i.slot, j] == 1:
                return self.flights[j]

    @staticmethod
    def is_in_list(list_to_check, elem):
        for el in list_to_check:
            if np.array_equiv(el, elem):
                return True
        return False

    def print_offers(self):
        tuples_found = []
        for off in self.offers:
            if not self.is_in_list(tuples_found, off[1]):
                airA = off[0]
                airB = self.which_airline(self.find_match(off[1][0]))
                print("{0:^5}".format(str(airA)), "{0:^15}".format(str(airB)))
                new_tuple = []
                for flight in off[1]:
                    match = self.find_match(flight)
                    print("{0:^5}".format(flight.name), " -> ", "{0:^5}".format(match.name),
                          " -> ", "{0:^5}".format(self.find_match(match).name))
                    new_tuple.append(self.find_match(flight))
                tuples_found.append(off[1])
                tuples_found.append(new_tuple)


# df = pd.read_csv("ruiz.csv")
# df["cost"] = np.random.uniform(1,15,df.shape[0])
#
# model = ModelStructure(df.iloc[0:10],lambda x,y: x*y, "test")
# print(model.flights)