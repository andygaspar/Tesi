import numpy as np
from itertools import product


class ModelStructure:

    def compute_delays(self):
        delays = np.zeros((self.slot_indexes.shape[0], self.slot_indexes.shape[0]))
        for flight, j in product(self.flights, self.slot_indexes):
            delays[flight.slot, j] = abs(self.gdp_schedule[j] - flight.eta)
        return delays

    @staticmethod
    def delay_cost(flight, delay):
        return flight.cost*delay**2

    def __init__(self, int_df):

        self.df = int_df

        self.slot_indexes = self.df["slot"].to_numpy()

        self.gdp_schedule = self.df["gdp schedule"].to_numpy()

        from Programma.ModelStructure import airlineList as airList, flightList as fll

        self.airlines = airList.make_airlines_list(self)

        self.num_airlines = len(np.unique(self.df["airline"]))

        self.flights = fll.make_flight_list(self)

        fll.assign_flight_num(self.flights)

        self.num_flights = len(self.flights)

        self.delays = self.compute_delays()

        self.empty_slots = self.df[int_df["flight"] == "Empty"]["slot"].to_numpy()

        self.solution_array = None

        self.solution = None

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def print_schedule(self):
        print(self.df)

    def print_solution(self):
        print(self.solution_df)

    def find_match(self, i):
        for j in self.slot_indexes[self.slot_indexes != i]:
            if self.solutionX[i.slot, j] == 1:
                return self.flights[j]
