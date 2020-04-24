import numpy as np
from Programma.Flight import flight as fl


class ModelFlight(fl.Flight):

    def __init__(self, line, airline, model):

        super().__init__(line, airline, model)

        self.priority = line["priority"]

        self.preference = None

    def set_preference(self, sum_priorities, f):
        self.preference = self.compute_preference(self.airline.num_flights, sum_priorities, f)

    def compute_preference(self, num_flights, sum_priorities, f):
        return f(self.priority, num_flights) / sum_priorities

    def set_priority(self, priority):
        self.priority = priority

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def compute_compatible_slots(self, df):
        try:
            second_comp_slot = df[df["gdp schedule"] > self.eta].iloc[0]["slot"]
            compatible_arrival_times = df[df["slot"] >= second_comp_slot - 1]["gdp schedule"].to_numpy()
            compatible_slots = df[df["slot"] >= second_comp_slot - 1]["slot"].to_numpy()
            return compatible_arrival_times, compatible_slots
        except IndexError:
            try:
                second_comp_slot = df[df["gdp schedule"] == self.eta].iloc[0]["slot"]
                compatible_arrival_times = df[df["slot"] >= second_comp_slot]["gdp schedule"].to_numpy()
                compatible_slots = df[df["slot"] >= second_comp_slot]["slot"].to_numpy()
                return compatible_arrival_times, compatible_slots
            except IndexError:
                raise IndexError("No available slot for flight ",self.name)




