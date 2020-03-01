from Programma.ModelStructure import airlineList as airll, flightList as fll

import numpy as np
from itertools import product
import sys


class ModelStructure:

    def compute_delays(self):
        delays = np.zeros((self.slot_indexes.shape[0], self.slot_indexes.shape[0]))
        for flight, j in product(self.flights, self.slot_indexes):
            delays[flight.slot, j] = abs(self.gdp_schedule[j] - flight.eta)
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

        self.solution_array = None

        self.solution = None

        self.initial_objective_value = sum([self.score(flight,flight.slot) for flight in self.flights])

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def score(self, flight, j):
        return (flight.preference*self.delays[flight.slot, j]**2)/2

    def print_schedule(self):
        print(self.df)

    def print_solution(self):
        print(self.solution_df)

    def find_match(self, i):
        for j in self.slot_indexes[self.slot_indexes != i]:
            if self.solutionX[i.slot, j] == 1:
                return self.flights[j]




