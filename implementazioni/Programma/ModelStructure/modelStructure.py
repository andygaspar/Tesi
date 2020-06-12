import numpy as np
from itertools import product


class ModelStructure:

    def compute_delays(self):
        delays = np.zeros((self.slotIndexes.shape[0], self.slotIndexes.shape[0]))
        for flight, j in product(self.flights, self.slotIndexes):
            delays[flight.slot, j] = abs(self.gdp_schedule[j] - flight.eta)
        return delays

    @staticmethod
    def delay_cost(flight, delay):
        return (flight.cost * delay ** 2)/2

    def __init__(self, df_init, cost_kind):

        self.df = df_init

        self.slotIndexes = self.df["slot"].to_numpy()

        self.gdp_schedule = self.df["gdp schedule"].to_numpy()

        from Programma.ModelStructure.Flight import flightList as fll
        from Programma.ModelStructure.Airline import airlineList as airList

        self.cost_kind = cost_kind

        self.airlines = airList.make_airlines_list(self)

        self.num_airlines = len(np.unique(self.df["airline"]))

        self.flights = fll.make_flight_list(self)

        fll.assign_flight_num(self.flights)

        self.num_flights = len(self.flights)

        self.delays = self.compute_delays()

        self.initial_total_costs = self.compute_costs(self.flights, "initial")

        self.empty_slots = self.df[self.df["flight"] == "Empty"]["slot"].to_numpy()

        self.mipSolution = None

        self.solution_array = None

        self.solution = None

        self.solutionDf = None

        self.report = None

    def cost_function(self, flight, j):
        from Programma.ModelStructure.Costs.costs import cost_function as cf
        return cf(self, flight, j)

    def compute_costs(self, flights, which):
        if which == "initial":
            return sum([self.cost_function(flight, flight.slot) for flight in flights])
        if which == "final":
            return sum([self.cost_function(flight, flight.new_slot) for flight in flights])

    def __str__(self):
        return str(self.airlines)

    def __repr__(self):
        return str(self.airlines)

    def print_schedule(self):
        print(self.df)

    def print_solution(self):
        print(self.solutionDf)

    def get_flight_by_slot_index(self, i):
        for flight in self.flights:
            if flight.slot == i:
                return flight

    def get_flight_name(self, f_name):
        for flight in self.flights:
            if flight.name == f_name:
                return flight

    def find_match(self, i):
        for j in self.slotIndexes[self.slotIndexes != i]:
            if self.mipSolution[i.slot, j] == 1:
                return self.flights[j]


