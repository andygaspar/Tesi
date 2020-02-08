import flight as fl
import airline as air

import numpy as np
import pandas as pd
from itertools import combinations, product
import sys


# noinspection PyPep8Naming,SpellCheckingInspection
class ModelStructure:

    def make_flight_list(self, df):
        flight_list = []
        for i in range(self.num_flights):
            line = df.iloc[i]
            if line["flight"] != "Empty":
                comp_slots = self.compute_compatible_slots(line["eta"])
                not_comp_slots = np.setdiff1d(self.slots,comp_slots)
                flight_list.append(fl.Flight(line["slot"], line["flight"], line["airline"], line["eta"], line["udpp"],
                                             line["priority"], comp_slots, not_comp_slots, line["costs"]))

        return np.array(flight_list)

    def make_airline_list(self, df):
        airline_list = []
        i = 0
        for airline in np.unique(df["airline"]):
            if airline != "Empty":
                airline_list.append(air.Airline(airline, i,
                                                [flight for flight in self.flights if flight.airline == airline],
                                                df[df["airline"] == airline]["priority"].to_numpy(), self.f))
                i += 1

        return airline_list

    def compute_delays(self):
        delays = np.zeros((self.num_flights, self.num_flights))
        for flight, j in product(self.flights, self.slots):
            delays[flight.slot, j] = abs(self.schedule[j] - flight.slot)
        return delays

    def compute_compatible_slots(self, eta):
        second_comp_slot = self.df[self.df["udpp"] > eta].iloc[0]["slot"]
        return self.df[self.df["slot"] >= second_comp_slot-1]["slot"].to_numpy()

    def __init__(self, df, f, model_name):

        self.e = sys.float_info.min

        self.df = df

        self.f = f

        self.num_flights = df.shape[0]

        self.slots = np.array(df["slot"])

        self.flights = self.make_flight_list(self.df)

        self.num_airlines = len(np.unique(self.df["airline"]))

        self.airlines = self.make_airline_list(self.df)

        self.empty_slots = self.df[df["flight"] == "Empty"]["slot"].to_numpy()

        self.schedule = self.df["udpp"]

        self.delays = self.compute_delays()

        #
        # self.ETA = np.array(ETA)
        # self.schedule = np.array(schedule)
        # self.ETA_index = self.compute_ETA_index(self.ETA)
        #
        # self.slots = np.array([i for i in range(len(self.schedule))])
        # self.delays = self.compute_delays()
        # for a in self.airlines:
        #     a.set_preferences(f)
        #
        self.solution_schedule = []
        # self.solutionX = None
        # self.solutionC = None
        #
        # self.offers = []

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def score(self, flight, j):
        return self.delays[flight.slot, j] * flight.preference

    def which_airline(self, flight):
        for airl in self.airlines:
            if flight in airl.flights:
                return airl

    def get_flights_name(self, i):
        return self.which_airline(i).flights_name[i]

    def print_schedule(self):
        print("{0:^10}".format("AIRLINE"), "{0:^10}".format("FLIGHT"),
              "{0:^10}".format("ETA"), "{0:^10}".format("DELAY"), "{0:^10}".format("COSTS"))

        for i in self.slots:
            print("{0:^10}".format(str(self.which_airline(i))),
                  "{0:^10}".format(self.which_airline(i).flights_name[i]),
                  "{0:^10}".format(self.ETA[i]),
                  "{0:^10}".format(self.delays[i, i]),
                  "{0:^10}".format(self.which_airline(i).preferences[i] * self.delays[i, i]))

    def print_solution(self):
        print("{0:^10}".format("AIRLINE"), "{0:^10}".format("FLIGHT"),
              "{0:^10}".format("ETA"), "{0:^10}".format("DELAY"), "{0:^10}".format("COSTS"))

        for sol in self.solution_schedule:
            print("{0:^10}".format(str(self.which_airline(sol[0]))),
                  "{0:^10}".format(self.which_airline(sol[0]).flights_name[sol[0]]),
                  "{0:^10}".format(self.ETA[sol[0]]),
                  "{0:^10}".format(self.delays[sol[0], sol[1]]),
                  "{0:^10}".format(self.which_airline(sol[0]).costs[sol[0]] * self.delays[sol[0], sol[1]]))

    def find_match(self, i):
        for j in self.slots[self.slots != i]:
            if self.solutionX[i, j].x == 1:
                return j

    @staticmethod
    def is_in_list(list_to_check, elem):
        for el in list_to_check:
            if np.array_equiv(el, elem):
                return True
        return False

    def print_offers(self):
        tuple_found = []
        for off in self.offers:
            if not self.is_in_list(tuple_found, off[1]):
                airA = off[0]
                airB = self.which_airline(self.find_match(off[1][0]))
                print("{0:^5}".format(str(airA)), "{0:^15}".format(str(airB)))
                new_tuple = []
                for flight in off[1]:
                    match = self.find_match(flight)
                    print("{0:^5}".format(airA.flights_name[flight]), " -> ", "{0:^5}".format(airB.flights_name[match]),
                          " -> ", "{0:^5}".format(airA.flights_name[self.find_match(match)]))
                    new_tuple.append(self.find_match(flight))
                tuple_found.append(off[1])
                tuple_found.append(np.sort(new_tuple))
