import numpy as np


class Flight:

    def __init__(self, line, airline, model):

        self.slot = line["slot"]

        self.name = line["flight"]

        self.airline = airline

        self.eta = line["eta"]

        self.gdp_arrival = line["gdp schedule"]

        self.cost = line["cost"]

        self.compatible_arrival_time, self.compatible_slots = self.compute_compatible_slots(model.df)

        self.not_compatible_slots = np.setdiff1d(model.df["slot"], self.compatible_slots)

        self.priority = line["priority"]

        self.preference = self.compute_preference(self.airline.num_flights, self.airline.sum_priorities, model.f)

    def compute_preference(self, num_flights, sum_priorities, f):
        return f(self.priority, num_flights) / sum_priorities

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


