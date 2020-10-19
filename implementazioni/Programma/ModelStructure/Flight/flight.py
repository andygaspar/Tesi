import numpy as np
from Programma.ModelStructure.Slot.slot import Slot


class Flight:

    def __init__(self, line, airline, model):

        self.slot = Slot(line["slot"], line["gdp schedule"])

        self.num = line["num"]

        self.newSlot = None

        self.name = line["flight"]

        self.airline = airline

        self.eta = line["eta"]

        self.eta_slot = len(model.gdp_schedule[model.gdp_schedule <= self.eta]) - 1

        self.gdp_arrival = line["gdp schedule"]

        self.new_arrival = None

        self.cost = line["cost"]

        self.compatible_arrival_time, self.compatible_slots = self.compute_compatible_slots(model.df)

        self.not_compatible_slots = np.setdiff1d(model.df["slot"], self.compatible_slots)

        self.localNum = None

        # UDPP attributes ***************

        self.UDPPLocalSlot = None

        self.UDPPlocalSolution = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_num(self, i):
        self.num = i

    def set_local_num(self, i):
        self.localNum = i

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
                raise IndexError("No available slot for flight ", self.name)
